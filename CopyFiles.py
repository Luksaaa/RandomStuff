import os
import shutil
import subprocess

def robocopy(source, destination):
    cmd = [
        "robocopy",
        source,
        destination,
        "/E",
        "/MT:32",
        "/R:3",
        "/W:5"
    ]
    subprocess.run(cmd, shell=True)

def xcopy(source, destination):
    cmd = f'xcopy "{source}" "{destination}" /E /I /H /Y'
    os.system(cmd)

def shutil_copy(source, destination):
    if os.path.isdir(source):
        shutil.copytree(source, destination, dirs_exist_ok=True)
    else:
        shutil.copy2(source, destination)

def main():
    print("====================================")
    print(" FILE COPY TOOL (CMD / PYTHON)")
    print("====================================")
    print("1 - ROBOCOPY (FASTEST)")
    print("2 - XCOPY")
    print("3 - PYTHON SHUTIL")
    print("====================================")

    choice = input("Choose method (1/2/3) --> ").strip()

    source = input("Enter SOURCE path --> ").strip('"')
    destination = input("Enter DESTINATION path --> ").strip('"')

    if not os.path.exists(source):
        print(" Source path does not exist!")
        return

    print("\n Copying...\n")

    if choice == "1":
        robocopy(source, destination)
    elif choice == "2":
        xcopy(source, destination)
    elif choice == "3":
        shutil_copy(source, destination)
    else:
        print(" Invalid option!")
        return

    print("\n Copy completed!")

if __name__ == "__main__":
    main()
