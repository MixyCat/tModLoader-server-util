import os
import subprocess
import sys
from time import sleep

tModLoaderServer_bat = (r"C:\Program Files (x86)"
                        r"\Steam\steamapps\common\tModLoader\start-tModLoaderServer.bat")
custom_serverconfig = os.path.join(
    os.path.dirname(sys.argv[0]),
    "custom_serverconfig.txt"
)


def wait_exit(status_code: int):
    input("Press Enter to exit...")
    sys.exit(status_code)


def get_modpacks_folder():
    user_path = os.path.expanduser("~")
    ending_path = r"Documents\My Games\Terraria\tModLoader\Mods\ModPacks"
    modpacks_folder_paths = [
        os.path.join(user_path, "OneDrive", ending_path),
        os.path.join(user_path, ending_path)
    ]

    for path in modpacks_folder_paths:
        if os.path.isdir(path):
            return path
    return None


def main():
    # Check for start-tModLoaderServer.bat file and ModPacks folder.
    if not os.path.isfile(tModLoaderServer_bat):
        print("start-tModLoaderServer.bat file not found!")
        wait_exit(1)

    modpacks_folder = get_modpacks_folder()
    if not os.path.isdir(modpacks_folder):
        print("ModPacks folder not found!")
        wait_exit(1)

    # Obtain valid ModPacks from its folder.
    modpacks = []
    for root, dirnames, filenames in os.walk(modpacks_folder):
        # Only proceed when the current root is in the Mods folder.
        if not os.path.basename(root) == "Mods":
            continue

        for name in filenames:
            if name == "enabled.json" and os.path.exists(os.path.join(root, name)):
                # Store the modpack name and its enabled.json path as a tuple.
                modpack_name = root.split("\\")[-2]
                modpacks.append((modpack_name, os.path.join(root, name)))
                break

    # Display the selection of possible modpacks you want to start the server with.
    SPACING = 20
    option = None
    while True:
        print("Select which modpack you want to start your tModLoader server with.\n")

        for i in range(len(modpacks)):
            modpack_name = modpacks[i][0]
            number = str(i+1)
            print(number.ljust(SPACING) + modpack_name)
        print("d".ljust(SPACING) + "Start server with no modpacks.")
        print("q".ljust(SPACING) + "Quit")

        print()
        option = input("Input option: ")

        # Quit if you select that option.
        if option == "q" or option == "Q":
            print("Exiting...")
            sleep(1)
            sys.exit(0)

        # Input validation here.
        valid_option = option == "d" or option == "D" or \
            (option.isnumeric() and 0 < int(option) <= len(modpacks))

        if valid_option:
            break

        print("\nThis option is not valid! Try again...\n")


    # Create a custom serverconfig file to open the start-tModLoader.bat file with. Or not with option d.
    if option == "d" or option == "D":
        subprocess.Popen([tModLoaderServer_bat])
        sys.exit(0)

    selected_modpack = modpacks[int(option)-1][1]
    with open(custom_serverconfig, "w") as f:
        f.write(f"modpack={selected_modpack}")

    subprocess.Popen([tModLoaderServer_bat, "-config", custom_serverconfig, "-nosteam"])


if __name__ == '__main__':
    main()
