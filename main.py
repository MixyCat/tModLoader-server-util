import os
from pathlib import Path
import subprocess
import sys
from time import sleep

# Initialize the tModLoaderServer.ssh file path, the busybox executable and the custom server config path.
tModLoaderServer_sh = (Path(r"C:\Program Files (x86)\Steam\steamapps\common\tModLoader\start-tModLoaderServer.sh").resolve())
busybox_exe = (Path(r"C:\Program Files (x86)\Steam\steamapps\common\tModLoader\LaunchUtils\busybox64.exe").resolve())

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    exec_path = Path(sys.executable)
else:
    exec_path = Path(__file__)

CUSTOM_SERVERCONFIG = exec_path.parent / "custom_serverconfig.txt"


def wait_exit(status_code: int) -> None:
    input("Press Enter to exit...")
    sys.exit(status_code)


def get_modpacks_folder() -> Path | None:
    ending_path = r"Documents\My Games\Terraria\tModLoader\Mods\ModPacks"
    modpacks_folder_paths = [
        Path.home() / "OneDrive" / ending_path,
        Path.home() / ending_path
    ]

    for path in modpacks_folder_paths:
        if path.is_dir():
            return path
    return None


def get_worlds_folder() -> Path | None:
    ending_path = r"Documents\My Games\Terraria\tModLoader\Worlds"
    worlds_folder_paths = [
        Path.home() / "OneDrive" / ending_path,
        Path.home() / ending_path
    ]

    for path in worlds_folder_paths:
        if path.is_dir():
            return path
    return None


# Menu for what modpack you want to start the server with.
def modpack_context_menu(modpacks_folder: Path) -> None:
    # Obtain valid ModPacks from its folder.
    modpacks = []
    for modpack_dir in modpacks_folder.iterdir():
        enabled_json: Path = modpack_dir / "Mods" / "enabled.json"
        if not enabled_json.exists():
            continue

        # Store the modpack name and its enabled.json path as a tuple.
        modpacks.append((modpack_dir.name, enabled_json))

    if not modpacks:
        print("There are no current modpacks in your directory! Using currently enabled mods instead...")
        sleep(1)
        return

    # Display the selection of possible modpacks you want to start the server with.
    SPACING = 20
    while True:
        print("Select which modpack you want to start your tModLoader server with.\n")

        for i in range(len(modpacks)):
            modpack_name = modpacks[i][0]
            number = str(i+1)
            print(number.ljust(SPACING) + modpack_name)
        print("d".ljust(SPACING) + "Start server with no modpacks.")
        print("q".ljust(SPACING) + "Quit")

        option = input("\nInput option: ")
        if option == "q" or option == "Q":
            print("Exiting...")
            sleep(1)
            sys.exit(0)
        elif option == "d" or option == "D":
            return
        elif option.isnumeric() and 0 < int(option) <= len(modpacks):
            selected_modpack = modpacks[int(option)-1][1]
            with open(CUSTOM_SERVERCONFIG, 'a') as f:
                f.write(f"modpack={selected_modpack}\n")
            return
        else:
            print("\nThis option is not valid! Try again...\n")


def world_context_menu(worlds_folder: Path) -> None:
    # Obtain valid worlds from the worlds folder.
    worlds = []
    for child in worlds_folder.iterdir():
        curr_path: Path = child
        if curr_path.exists() and curr_path.suffix == ".wld":
            worlds.append(curr_path)

    if not worlds:
        print("There are no current worlds in your directory! Using the default context menu instead...")
        sleep(1)
        return

    # Display the selection of possible worlds you want to start the server with.
    SPACING = 20
    while True:
        print("Select which world you want to start your tModLoader server with.\n")

        for i in range(len(worlds)):
            world_name = worlds[i].stem
            number = str(i+1)
            print(number.ljust(SPACING) + world_name)
        print("d".ljust(SPACING) + "Start server with default context.")
        print("q".ljust(SPACING) + "Quit")

        option = input("\nInput option: ")
        if option == "q" or option == "Q":
            print("Exiting...")
            sleep(1)
            sys.exit(0)
        elif option == "d" or option == "D":
            return
        elif option.isnumeric() and 0 < int(option) <= len(worlds):
            selected_world = worlds[int(option)-1]
            with open(CUSTOM_SERVERCONFIG, 'a') as f:
                f.write(f"world={selected_world}\n")
            return
        else:
            print("\nThis option is not valid! Try again...\n")


def main():
    # Check for start-tModLoaderServer.sh file, busybox executable and ModPacks folder.
    if not tModLoaderServer_sh.exists():
        print("start-tModLoaderServer.sh file not found!")
        wait_exit(1)
    
    if not busybox_exe.exists():
        print("busybox.exe executable not found!")
        wait_exit(1)

    modpacks_folder = get_modpacks_folder()
    if not modpacks_folder:
        print("ModPacks folder not found!")
        wait_exit(1)

    worlds_folder = get_worlds_folder()
    if not worlds_folder:
        print("tModLoader Worlds folder not found!")
        wait_exit(1)

    # Remove existing custom server config if it exists.
    if CUSTOM_SERVERCONFIG.exists():
        CUSTOM_SERVERCONFIG.unlink()

    modpack_context_menu(modpacks_folder)
    world_context_menu(worlds_folder)

    # Start the tModLoaderServer.bat file with the custom config options.
    args = [busybox_exe, "bash", tModLoaderServer_sh, "-config", CUSTOM_SERVERCONFIG, "-nosteam"]
    subprocess.run(args)
    print("Done!")
    input("Press enter to exit...")


if __name__ == '__main__':
    main()
