import subprocess
from datetime import datetime
from time import sleep


def open_all_apps(app_list):
    for app in app_list:
        start_app(app, 10)
        stop_app(app)


def start_app(app_to_start, capture_time=20):
    try:
        subprocess.run(["adb", "shell", "monkey -p", app_to_start, "-c android.intent.category.LAUNCHER 1"],
                       check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print("Click to proceed")
        proceed = str(input())

    except subprocess.SubprocessError as start_app_err:
        print(f'Start {app_to_start} at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - '
                      f'Error message: {str(start_app_err)}')
    stop_app(app_to_start)


def stop_app(app_to_stop):
    try:
        subprocess.run(["adb", "shell", "am force-stop", app_to_stop], check=True, stderr=False)
    except subprocess.SubprocessError as stop_app_err:
        print(f'Stop {app_to_stop} at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - '
                      f'Error message: {str(stop_app_err)}')
    sleep(1)


if __name__ == '__main__':
    with open('../phone/apps/packages_ow.txt', 'r', encoding='utf-8') as file:
        packages = file.read().splitlines()
    print(packages)
    open_all_apps(packages)