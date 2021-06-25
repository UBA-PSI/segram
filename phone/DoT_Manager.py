import subprocess
from time import sleep
import logging
from config import DOT_RESOLVER


class DoT_Manager:
    def __init__(self):
        self.resolver = DOT_RESOLVER

    def disable_private_dns(self):
        subprocess.run(["adb", "shell", "settings put global private_dns_mode off"])
        sleep(0.5)
        logging.info(f"disabled private dns")

    def change_resolver(self, new_resolver):
        cmd_resolver = "settings put global private_dns_specifier " + new_resolver
        subprocess.run(["adb", "shell", cmd_resolver])
        sleep(1)
        logging.info(f"changed the DoT resolver to {new_resolver}{chr(10)}")

    def enable_private_dns(self):
        subprocess.run(["adb", "shell", "settings put global private_dns_mode hostname"])
        sleep(0.5)
        logging.info(f"enabled private dns")

    def get_status(self):
        sleep(0.5)
        status = subprocess.run(["adb", "shell", "settings list global | grep private_dns_mode"], capture_output=True,
                                check=False)
        if "off" in str(status.stdout):
            return False
        if "private_dns_mode=hostname" in str(status.stdout) or "private_dns_mode=opportunistic" in str(status.stdout):
            return True
        sleep(0.5)

