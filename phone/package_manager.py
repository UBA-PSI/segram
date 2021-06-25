import subprocess
from config import DEL_APPS


def deinstall_apps():
    with open(DEL_APPS, 'r', encoding='utf-8') as file:
        packages = file.read().splitlines()
    for package in packages:
        subprocess.run(["adb", "shell", "pm uninstall", package])


if __name__ == '__main__':
    deinstall_apps()