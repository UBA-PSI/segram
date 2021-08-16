import subprocess
from datetime import datetime
from time import sleep


def open_app_often(app_list, save_path):
    for app in app_list:
        for i in range(10):
            capture(app, save_path, 'dns.google')
            sleep(5)
            start_app(app)
            stop_app(app)
            kill_tcpdump()
            sleep(5)


def capture(called_app, directory, dns_resolver_name):
    pcap = f"{directory}/{datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}--{dns_resolver_name}--{called_app}.pcap"
    try:
        cmd = "tcpdump -i wlp5s0 not broadcast and not multicast and not arp and not icmp -w" + pcap
        subprocess.Popen(["ssh", "bluebox", cmd])
    except subprocess.CalledProcessError as start_capture_error:
        pass
        exit()
    sleep(2)
    start_app(called_app)


def start_app(app_to_start, capture_time=20):
    try:
        subprocess.run(["adb", "shell", "monkey -p", app_to_start, "-c android.intent.category.LAUNCHER 1"],
                       check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        sleep(capture_time)
    except subprocess.SubprocessError as start_app_err:
        print(f'Start {app_to_start} at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - '
              f'Error message: {str(start_app_err)}')


def stop_app(app_to_stop):
    try:
        subprocess.run(["adb", "shell", "am force-stop", app_to_stop], check=True, stderr=False)
    except subprocess.SubprocessError as stop_app_err:
        print(f'Stop {app_to_stop} at {datetime.now().strftime("%d-%m-%Y--%H-%M-%S")} - '
              f'Error message: {str(stop_app_err)}')
    sleep(1)


def make_dir_remote(save_path):
    subprocess.Popen(["ssh", "hostname", "mkdir", save_path])
    sleep(1)


def kill_tcpdump():
    subprocess.run(["ssh", "hostname", "killall tcpdump"], check=True, stderr=False)


if __name__ == '__main__':
    save_path = "/home/cache_test/"
    make_dir_remote(save_path)
    open_app_often(['de.spiegel.android.app.spon'], save_path)
