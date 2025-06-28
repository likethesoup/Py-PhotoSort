import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import calendar

def get_photo_date(image_path):
    """Extract the date taken from photo metadata"""
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Get EXIF data
        exifdata = image.getexif()
        
        # Look for date taken in EXIF data
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            
            # Common date tags
            if tag in ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']:
                try:
                    # Parse the date string (format: "YYYY:MM:DD HH:MM:SS")
                    date_obj = datetime.strptime(data, "%Y:%m:%d %H:%M:%S")
                    return date_obj
                except:
                    continue
        
        # If no EXIF date found, try file modification date
        modification_time = os.path.getmtime(image_path)
        return datetime.fromtimestamp(modification_time)
        
    except Exception as e:
        print(f"Error reading date from {image_path}: {e}")
        return None

def create_folder_structure(base_path, year, month):
    """Create year and month folders if they don't exist"""
    month_name = calendar.month_name[month]
    year_folder = os.path.join(base_path, str(year))
    month_folder = os.path.join(year_folder, f"{year}-{month:02d}-{month_name}")
    
    # Create directories if they don't exist
    os.makedirs(month_folder, exist_ok=True)
    
    return month_folder

def organize_photos(source_folder, destination_folder=None):
    """Main function to organize photos"""
    
    if destination_folder is None:
        destination_folder = source_folder
    
    # Supported image extensions
    supported_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.gif', '.webp', '.heic', '.raw', '.cr2', '.nef', '.arw'}
    
    # Create a folder for photos without dates
    no_date_folder = os.path.join(destination_folder, "No_Date_Found")
    
    moved_count = 0
    no_date_count = 0
    error_count = 0
    
    print("Starting photo organization...")
    print(f"Source folder: {source_folder}")
    print(f"Destination folder: {destination_folder}")
    print("-" * 50)
    
    # Process all files in the source folder
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        
        # Skip if it's a directory
        if os.path.isdir(file_path):
            continue
            
        # Check if it's a supported image file
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in supported_extensions:
            continue
            
        print(f"Processing: {filename}")
        
        # Get the photo date
        photo_date = get_photo_date(file_path)
        
        if photo_date:
            # Create the appropriate folder structure
            month_folder = create_folder_structure(destination_folder, photo_date.year, photo_date.month)
            
            # Move the file
            new_path = os.path.join(month_folder, filename)
            
            # Handle duplicate filenames
            counter = 1
            original_new_path = new_path
            while os.path.exists(new_path):
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_{counter}{ext}"
                new_path = os.path.join(month_folder, new_filename)
                counter += 1
            
            try:
                shutil.move(file_path, new_path)
                moved_count += 1
                print(f"  → Moved to: {os.path.relpath(new_path, destination_folder)}")
            except Exception as e:
                print(f"  → Error moving file: {e}")
                error_count += 1
        else:
            # Move to no date folder
            os.makedirs(no_date_folder, exist_ok=True)
            new_path = os.path.join(no_date_folder, filename)
            
            # Handle duplicate filenames
            counter = 1
            while os.path.exists(new_path):
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_{counter}{ext}"
                new_path = os.path.join(no_date_folder, new_filename)
                counter += 1
            
            try:
                shutil.move(file_path, new_path)
                no_date_count += 1
                print(f"  → Moved to: No_Date_Found folder")
            except Exception as e:
                print(f"  → Error moving file: {e}")
                error_count += 1
    
    # Print summary
    print("-" * 50)
    print("Organization complete!")
    print(f"Photos organized by date: {moved_count}")
    print(f"Photos without date info: {no_date_count}")
    print(f"Errors encountered: {error_count}")

if __name__ == "__main__":
    # CONFIGURATION - CHANGE THESE PATHS
    SOURCE_FOLDER = r"C:\Users\liket\OneDrive\Pictures\Camera Roll"  # Change this to your photo folder path
    
    print("Photo Organizer Script")
    print("=" * 50)
    
    # Verify the source folder exists
    if not os.path.exists(SOURCE_FOLDER):
        print(f"Error: Source folder '{SOURCE_FOLDER}' does not exist.")
        print("Please update the SOURCE_FOLDER path in the script.")
        input("Press Enter to exit...")
        exit()
    
    # Ask for confirmation
    print(f"This will organize photos in: {SOURCE_FOLDER}")
    print("Photos will be MOVED (not copied) into year/month folders.")
    print("Make sure you have a backup of your photos before proceeding!")
    
    confirm = input("\nDo you want to proceed? (yes/no): ").lower().strip()
    
    if confirm in ['yes', 'y']:
        organize_photos(SOURCE_FOLDER)
    else:
        print("Operation cancelled.")
    
    input("\nPress Enter to exit...")
