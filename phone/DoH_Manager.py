import subprocess
from time import sleep
from datetime import datetime
import logging
from config import DOH_RESOLVER

# This implementation uses ADB commands to control the Intra app, i.e., to set DoH resolvers.
# For the used ADB commands, we were inspired by multiple references, e.g.:
# Yaghmour, K. (2013). Embedded Android: Porting, Extending, and Customizing. " O'Reilly Media, Inc.".
# https://developer.android.com/studio/command-line/adb

class Intra:

    def __init__(self):
        self.app = "app.intra"
        self.resolver = DOH_RESOLVER

    def launch_intra(self, sleep_time=0.5):
        try:
            subprocess.run(["adb", "shell", "monkey -p", self.app, "-c android.intent.category.LAUNCHER 1"],
                           check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            sleep(sleep_time)
        except subprocess.SubprocessError:
            logging.error(f'Starting {self.app} at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} failed')

    def enable_intra(self):
        self.launch_intra(1)
        # enable intra
        subprocess.run(["adb", "shell", "input tap 946 315"], check=True, stderr=False)
        logging.info("enabled intra...")
        sleep(0.2)
        # to home
        subprocess.run(["adb", "shell", "input keyevent KEYCODE_HOME"], check=True, stderr=False)

    def disable_intra(self):
        self.launch_intra()
        # disable intra
        subprocess.run(["adb", "shell", "input tap 946 315"], check=True, stderr=False)
        logging.info("disabled intra..." + "\n")
        sleep(0.2)
        # to home
        subprocess.run(["adb", "shell", "input keyevent KEYCODE_HOME"], check=True, stderr=False)

    def force_stop_intra(self):
        subprocess.run(["adb", "shell", "am force-stop app.intra"], check=True, stderr=False)

    def get_status(self):
        status = subprocess.run(["adb", "shell", "ip a"], capture_output=True, check=False)
        vpn_if = str(status.stdout).find('tun0')
        if vpn_if > 0:
            return True
        else:
            return False

    def change_resolver(self, resolver_name):
        self.launch_intra(1)
        # click on left corner
        subprocess.run(["adb", "shell", "input tap 369 319"], check=True, stderr=False)
        sleep(1)
        # click on settings
        subprocess.run(["adb", "shell", "input tap 66 157"], check=True, stderr=False)
        sleep(1)
        # click select doh
        subprocess.run(["adb", "shell", "input tap 184 283"], check=True, stderr=False)
        sleep(1)
        # click on select doh server
        subprocess.run(["adb", "shell", "input tap 522 305"], check=True, stderr=False)
        sleep(1)
        # click on user defined
        subprocess.run(["adb", "shell", "input tap 143 1161"], check=True, stderr=False)
        sleep(1)
        # click in text boc
        subprocess.run(["adb", "shell", "input tap 371 1242"], check=True, stderr=False)
        sleep(1)
        # intra switches to preset options if it knows url
        subprocess.run(["adb", "shell", "input text Sauerkraut"], check=True, stderr=False)
        sleep(1)
        # select text
        subprocess.run(["adb", "shell", "input touchscreen swipe 270 888 270 888 2000"], check=True, stderr=False)
        sleep(1)
        # delete text
        subprocess.run(["adb", "shell", "input keyevent KEYCODE_DEL"], check=True, stderr=False)
        sleep(1)
        # write doh name
        subprocess.run(["adb", "shell", "input text", resolver_name], check=True, stderr=False)
        sleep(1)
        # confirm
        subprocess.run(["adb", "shell", "input tap 864 1136"], check=True, stderr=False)
        sleep(1)
        # stop the app
        self.force_stop_intra()
        logging.info(f"changed the DoH resolver to {resolver_name}")
