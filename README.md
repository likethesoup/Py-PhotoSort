# Py-PhotoSort

A simple set of python scripts to help organize your photos:
  - photo_organizer.py sorts photos into folders by year and month
  - rename_folders.py renames subfolders within a folder to a standard formatting


HOW TO USE:


ORGANIZE PHOTOS

Looks at EXIF data for image files and then sorts them into folders by year then month (e.g. 2025/2025-01-January/photo1.jpg). It sorts one file at a time, so it can take a few hours if you have many thousands of photos.

  1. Copy photo_organizer.py to the folder that contains your photos.
  2. Open terminal or command prompt and run it: python photo_organizer.py
  3. Press y to proceed with sorting.


RENAME FOLDERS

Looks for folder names like 01-Jan, 01, Jan, January and renames to YYYY-MM-Month (e.g. 2025-01-January). To be extra safe, it will only look for subfolders within the folder the script is placed.

  1. Copy rename_folders.py to the folder than contains the subfolders that need renamed.
  2. Open terminal or command prompt and run it: python rename_folders.py
  3. Enter the year (e.g. 2025) that should be use for all subfolders.
  4. Press y to proceed with renaming.

