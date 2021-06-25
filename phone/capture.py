import subprocess
from datetime import datetime
from time import sleep
import DoH_Manager
import DoH_Manager_CP
import DoT_Manager
import logging
import random
from config import CACHING, SAVE_DIR, APPS, SSH_HOST, CAPTURE_TIME, DOH_IMPL

logging.basicConfig(level=logging.INFO, filename='capturing.log', filemode='a',
                    format='%(levelname)s - %(message)s')


def is_screen_on():
    try:
        screen_state = subprocess.run(["adb", "shell", "dumpsys display | grep 'mScreenState='"],
                                      capture_output=True, check=True)
        if "mScreenState=ON" in str(screen_state):
            return True
    except subprocess.SubprocessError as screen_err:
        logging.error(
            f'Screen on at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - Error message: {str(screen_err)}')
    return False


def press_power_button():
    try:
        subprocess.run(["adb", "shell", "input keyevent 26"], check=True)
    except subprocess.SubprocessError as pwr_bt:
        logging.error(f'Power Button at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - Error message: {str(pwr_bt)}')


def make_dir_remote(save_path):
    try:
        subprocess.Popen(["ssh", SSH_HOST, "mkdir", save_path])
    except subprocess.SubprocessError as e:
        logging.error(f'{SSH_HOST} mkdir at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - Error message: {str(e)}')
    sleep(1)


def disable_all_dns_before_start():
    dot_manager = DoT_Manager.DoT_Manager()
    intra = DoH_Manager.Intra()
    while dot_manager.get_status():
        logging.warning(f"---disable private DNS before launch at {datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}---")
        dot_manager.disable_private_dns()
        sleep(2)
    while intra.get_status():
        logging.warning(f"---disable Intra before launch at {datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}---")
        intra.disable_intra()
        sleep(2)


def clear_dns_cache():
    logging.info("clearing DNS cache...")
    subprocess.run(["adb", "shell", "svc wifi disable"])
    sleep(0.5)
    subprocess.run(["adb", "shell", "svc wifi enable"])
    connected = False
    while not connected:
        connectivity_state = subprocess.run(["adb", "shell", "dumpsys wifi | grep 'mNetworkInfo'"], capture_output=True)
        if 'state: CONNECTED/CONNECTED' in str(connectivity_state):
            connected = True
            # wait because of DNS queries for connectivity checks
            sleep(2)
        sleep(1)
    logging.info('DNS cache cleared...')


def sleep_when_caching(ttl_app, current_index):
    if current_index % 15 == 0 and current_index > 0:
        logging.info(f"{datetime.now().strftime('%d-%m-%Y--%H-%M-%S')} slept for {get_random_ttl(ttl_app)} seconds "
                     f"for {ttl_app}...")
        sleep(get_random_ttl(ttl_app))
    sleep(3)


def get_random_ttl(caller_pkg):
    random.seed(caller_pkg)
    # these values are among the fifty most used TTL values (4352/7069 TTLs are from these values)
    ttls = [60, 300, 20, 59, 27, 30, 26, 28, 15, 8, 1, 13, 23, 10, 56,
            180, 153, 21, 19, 53, 63, 32, 120, 25, 5, 46, 4, 29, 9, 58,
            12, 17, 218, 142, 140, 181, 168, 52, 195, 42, 150]
    random_ttl = random.choice(ttls)
    return random_ttl


def capture(called_app, directory, dns_resolver_name):
    pcap = f"{directory}/{datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}--{dns_resolver_name}--{called_app}.pcap"
    try:
        cmd = "tcpdump -i wlp5s0 not broadcast and not multicast and not arp and not icmp -w" + pcap
        logging.info("capturing...")
        subprocess.Popen(["ssh", SSH_HOST, cmd])
    except subprocess.CalledProcessError as start_capture_error:
        logging.error(f'Start tcpdump at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - '
                      f'Error message: {str(start_capture_error)}')
        exit()
    sleep(2)
    start_app(called_app)


def start_app(app_to_start, capture_time=CAPTURE_TIME):
    logging.info("starting app...")
    try:
        subprocess.run(["adb", "shell", "monkey -p", app_to_start, "-c android.intent.category.LAUNCHER 1"],
                       check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        logging.info(f"{datetime.now().strftime('%d-%m-%Y--%H-%M-%S')} {app_to_start} started...")
        sleep(capture_time)
    except subprocess.SubprocessError as start_app_err:
        logging.error(f'Start {app_to_start} at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - '
                      f'Error message: {str(start_app_err)}')
    stop_app(app_to_start)
    kill_tcpdump()


def stop_app(app_to_stop):
    try:
        subprocess.run(["adb", "shell", "am force-stop", app_to_stop], check=True, stderr=False)
    except subprocess.SubprocessError as stop_app_err:
        logging.error(f'Stop {app_to_stop} at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - '
                      f'Error message: {str(stop_app_err)}')
    logging.info(f"{datetime.now().strftime('%d-%m-%Y--%H-%M-%S')} {app_to_stop} killed..")
    sleep(1)


def kill_tcpdump():
    try:
        subprocess.run(["ssh", SSH_HOST, "killall tcpdump"], check=True, stderr=False)
    except subprocess.SubprocessError as stop_capture_err:
        logging.error(
            f'Tcpdump at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - Error message: {str(stop_capture_err)}')
    logging.info("tcpdump killed...")


def capture_udp_dns_traffic(app_list, save_dir):
    udp_dir = save_dir + "/" + "UDP"
    try:
        subprocess.Popen(["ssh", SSH_HOST, "mkdir", udp_dir])
    except subprocess.SubprocessError as dot_dir_err:
        logging.error(
            f'{SSH_HOST} UDP at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - Error message: {str(dot_dir_err)}')
    # part where UDP starts
    for app in app_list:
        clear_dns_cache()
        capture(app, udp_dir, "udp")


def capture_doh_traffic(apps_list, save_dir):
    pkgs_doh_shuffled = apps_list
    doh_dir = save_dir + "/" + "DoH"
    try:
        subprocess.Popen(["ssh", SSH_HOST, "mkdir", doh_dir])
    except subprocess.SubprocessError as doh_dir_err:
        logging.error(
            f'{SSH_HOST} DoH at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - Error message: {str(doh_dir_err)}')
    # part where DoH starts
    if DOH_IMPL == "pixel":
        intra = DoH_Manager.Intra()
    else:
        intra = DoH_Manager_CP.Intra()
    for resolver in intra.resolver:
        random.seed(resolver)
        random.shuffle(pkgs_doh_shuffled)
        intra.change_resolver(resolver)
        intra.enable_intra()
        while not intra.get_status():
            logging.warning(f"---had to enable intra at {datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}---")
            intra.enable_intra()
            sleep(2)
        resolver = resolver.split('/')[2]
        for index, app in enumerate(pkgs_doh_shuffled):
            if CACHING == 'DISABLED':
                clear_dns_cache()
            capture(app, doh_dir, resolver)
            if CACHING == 'ENABLED':
                sleep_when_caching(app, index)
        intra.disable_intra()
        while intra.get_status():
            logging.warning(f"---had to disable intra at {datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}---")
            intra.disable_intra()
            sleep(2)
    intra.force_stop_intra()


def capture_dot_traffic(app_list, save_dir):
    pkgs_dot_shuffled = app_list
    dot_dir = save_dir + "/" + "DoT"
    try:
        subprocess.Popen(["ssh", SSH_HOST, "mkdir", dot_dir])
    except subprocess.SubprocessError as dot_dir_err:
        logging.error(
            f'{SSH_HOST} DoT at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - Error message: {str(dot_dir_err)}')
    dot_manager = DoT_Manager.DoT_Manager()
    # part where DoT starts
    dot_manager.enable_private_dns()
    while not dot_manager.get_status():
        logging.warning(f"---had to enable DoT at {datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}---")
        dot_manager.enable_private_dns()
        sleep(2)
    for resolver, ip in dot_manager.resolver:
        random.seed(resolver)
        random.shuffle(pkgs_dot_shuffled)
        dot_manager.change_resolver(resolver)
        for index, app in enumerate(pkgs_dot_shuffled):
            if CACHING == 'DISABLED':
                clear_dns_cache()
            capture(app, dot_dir, resolver)
            if CACHING == 'ENABLED':
                sleep_when_caching(app, index)
    dot_manager.disable_private_dns()


if __name__ == '__main__':
    for i in range(2):
        logging.info(f"Capture Round at {datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}{chr(10)}")
        if not is_screen_on():
            press_power_button()
        directory_to_save = SAVE_DIR + "files_" + datetime.now().strftime("%d-%m-%Y--%H-%M-%S")
        make_dir_remote(directory_to_save)
        with open(APPS, 'r', encoding='utf-8') as file:
            packages = file.read().splitlines()

        disable_all_dns_before_start()
        # capture_udp_dns_traffic(packages, directory_to_save)
        capture_doh_traffic(packages, directory_to_save)
        capture_dot_traffic(packages, directory_to_save)
        press_power_button()
        sleep(1000)
