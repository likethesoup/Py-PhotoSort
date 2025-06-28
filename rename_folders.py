#!/usr/bin/env python3
"""
Script to rename folders in current directory to YYYY-MM-Month format.
Handles various input formats like 01, 01-Jan, 01-January, 06-Jun, 06-June, etc.
"""

import os
import re
from datetime import datetime

def get_month_info(month_str):
    """Convert month string to month number and full month name."""
    month_mappings = {
        # Short month names
        'jan': (1, 'January'),
        'feb': (2, 'February'),
        'mar': (3, 'March'),
        'apr': (4, 'April'),
        'may': (5, 'May'),
        'jun': (6, 'June'),
        'jul': (7, 'July'),
        'aug': (8, 'August'),
        'sep': (9, 'September'),
        'oct': (10, 'October'),
        'nov': (11, 'November'),
        'dec': (12, 'December'),
        # Full month names
        'january': (1, 'January'),
        'february': (2, 'February'),
        'march': (3, 'March'),
        'april': (4, 'April'),
        'june': (6, 'June'),
        'july': (7, 'July'),
        'august': (8, 'August'),
        'september': (9, 'September'),
        'october': (10, 'October'),
        'november': (11, 'November'),
        'december': (12, 'December')
    }
    
    month_lower = month_str.lower()
    return month_mappings.get(month_lower, (None, None))

def parse_folder_name(folder_name):
    """Parse folder name to extract month information."""
    # First check if it's just a numeric month (01, 02, ..., 12)
    if re.match(r'^\d{1,2}$', folder_name.strip()):
        try:
            month_num = int(folder_name.strip())
            if 1 <= month_num <= 12:
                month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                              'July', 'August', 'September', 'October', 'November', 'December']
                return month_num, month_names[month_num - 1]
        except ValueError:
            pass
    
    # Pattern to match formats like: 01-Jan, 01-January, 06-Jun, 06-June, etc.
    patterns = [
        r'^(\d{1,2})[-_\s]([a-zA-Z]+)$',  # 01-Jan, 01_January, 01 Jan
        r'^([a-zA-Z]+)[-_\s](\d{1,2})$',  # Jan-01, January_01, Jan 01
        r'^(\d{1,2})([a-zA-Z]+)$',        # 01Jan, 01January
        r'^([a-zA-Z]+)(\d{1,2})$',        # Jan01, January01
        r'^([a-zA-Z]+)$',                 # Just month name
    ]
    
    for pattern in patterns:
        match = re.match(pattern, folder_name.strip())
        if match:
            groups = match.groups()
            
            # Try to identify which group is the month
            for group in groups:
                month_num, month_name = get_month_info(group)
                if month_num is not None:
                    return month_num, month_name
    
    return None, None

def get_year_from_user():
    """Prompt user for the year to use in renaming."""
    while True:
        try:
            year = input("Enter the year to use for renaming (e.g., 2024): ").strip()
            year_int = int(year)
            
            # Basic validation - reasonable year range
            if 1900 <= year_int <= 2100:
                return year_int
            else:
                print("Please enter a year between 1900 and 2100.")
                
        except ValueError:
            print("Please enter a valid year (numbers only).")

def main():
    """Main function to rename folders."""
    print("Folder Date Renamer")
    print("=" * 20)
    print("This script will rename folders in the current directory to YYYY-MM-Month format.")
    print()
    
    # Get current directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Get all folders in current directory
    folders = [item for item in os.listdir(current_dir) 
              if os.path.isdir(os.path.join(current_dir, item))]
    
    if not folders:
        print("No folders found in the current directory.")
        return
    
    print(f"\nFound {len(folders)} folder(s):")
    for folder in folders:
        print(f"  - {folder}")
    
    # Parse folder names and show what would be renamed
    renameable_folders = []
    print("\nParsing folder names:")
    
    for folder in folders:
        month_num, month_name = parse_folder_name(folder)
        if month_num and month_name:
            renameable_folders.append((folder, month_num, month_name))
            print(f"  ✓ {folder} -> will become YYYY-{month_num:02d}-{month_name}")
        else:
            print(f"  ✗ {folder} -> could not parse date format")
    
    if not renameable_folders:
        print("\nNo folders with recognizable date formats found.")
        return
    
    print(f"\n{len(renameable_folders)} folder(s) can be renamed.")
    
    # Get year from user
    year = get_year_from_user()
    
    # Show preview of new names
    print(f"\nPreview of new names with year {year}:")
    for old_name, month_num, month_name in renameable_folders:
        new_name = f"{year}-{month_num:02d}-{month_name}"
        print(f"  {old_name} -> {new_name}")
    
    # Confirm before renaming
    print()
    confirm = input("Proceed with renaming? (y/N): ").strip().lower()
    
    if confirm not in ['y', 'yes']:
        print("Renaming cancelled.")
        return
    
    # Perform the renaming
    print("\nRenaming folders...")
    success_count = 0
    
    for old_name, month_num, month_name in renameable_folders:
        try:
            new_name = f"{year}-{month_num:02d}-{month_name}"
            old_path = os.path.join(current_dir, old_name)
            new_path = os.path.join(current_dir, new_name)
            
            # Check if target already exists
            if os.path.exists(new_path):
                print(f"  ✗ {old_name} -> {new_name} (target already exists)")
                continue
            
            os.rename(old_path, new_path)
            print(f"  ✓ {old_name} -> {new_name}")
            success_count += 1
            
        except OSError as e:
            print(f"  ✗ {old_name} -> {new_name} (error: {e})")
    
    print(f"\nCompleted! Successfully renamed {success_count} out of {len(renameable_folders)} folders.")

if __name__ == "__main__":
    main()