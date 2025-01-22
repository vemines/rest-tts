# delete_files.py
import os
import datetime

def delete_files(folder_paths):
    print(f"Starting file deletion at {datetime.datetime.now()}")
    for folder_path in folder_paths:
      print(f"Processing folder: {folder_path}")
      for filename in os.listdir(folder_path):
          file_path = os.path.join(folder_path, filename)
          try:
              if os.path.isfile(file_path):
                 os.unlink(file_path)
                 print(f"Deleted file: {file_path}")
          except Exception as e:
              print(f"Error deleting file {file_path}: {e}")
    print(f"Finished file deletion at {datetime.datetime.now()}")

if __name__ == "__main__":
    target_folders = ["output/etts", "output/gtts"]  # Change to your actual folder paths
    delete_files(target_folders)