# THIS SCRIPT DELETES HTML FILES IN A SPECIFIED DIRECTORY
import os
skip = input("Enter files to skip with space in between:").split()
directory = "D:\Landing Pages\potd"
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
for file in files:
    if os.path.splitext(file)[1]=='.html':
        if file in skip:
            print(f"Skipping {file}")
            continue

        os.remove(os.path.join(directory, file))
        print(f"Deleted {file}")

