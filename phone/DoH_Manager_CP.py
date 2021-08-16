from uiautomator import device as d
from time import sleep
from datetime import datetime
import subprocess
import logging
from config import DOH_RESOLVER

# This implementation uses uiautomator to control the Intra app, i.e., to set DoH resolvers.
# The implementation will probably only work if the language of the phone is German
# For other languages, you have to exchange the text parameters

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

    def change_resolver(self, resolver_name):
        # launch
        self.launch_intra()
        d(packageName=self.app, className="android.widget.ImageButton").click()
        sleep(1)
        d(packageName=self.app, className="android.widget.CheckedTextView", text="Einstellungen").click()
        sleep(1)
        d(packageName=self.app, className="android.widget.TextView", text="DNS-over-HTTPS-Server auswählen").click()
        sleep(1)
        d(packageName=self.app, className="android.widget.RadioButton", text="Benutzerdefinierte Server-URL").click()
        sleep(1)
        d(packageName=self.app, className="android.widget.EditText",
          resourceId="app.intra:id/custom_server_url").click()
        sleep(1)
        d(packageName=self.app, resourceId="app.intra:id/custom_server_url").clear_text()
        sleep(1)
        d(packageName=self.app, resourceId="app.intra:id/custom_server_url").set_text(resolver_name)
        sleep(1)
        d.press.back()
        sleep(1)
        d(packageName=self.app, className="android.widget.Button", resourceId="android:id/button1").click()
        sleep(1)
        d(packageName=self.app, className="android.widget.ImageButton").click()
        sleep(1)
        d.press.home()
        self.force_stop_intra()
        logging.info(f"changed the DoH resolver to {resolver_name}")

    def get_status(self):
        status = subprocess.run(["adb", "shell", "ip a"], capture_output=True, check=False)
        vpn_if = str(status.stdout).find('tun0')
        if vpn_if > 0:
            return True
        else:
            return False

    def enable_intra(self):
        # launch
        self.launch_intra()
        if not self.get_status():
            d(packageName=self.app, className="android.widget.Switch", resourceId="app.intra:id/dns_switch").click()
        logging.info("enabled intra...")
        sleep(0.2)
        d.press.home()

    def disable_intra(self):
        # launch
        self.launch_intra()
        if self.get_status():
            d(packageName=self.app, className="android.widget.Switch", resourceId="app.intra:id/dns_switch").click()
        logging.info("disabled intra..." + "\n")
        sleep(0.2)
        d.press.home()

    def force_stop_intra(self):
        subprocess.run(["adb", "shell", "am force-stop app.intra"], check=True, stderr=False)
