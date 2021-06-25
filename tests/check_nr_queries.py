import pyshark
import os
from multiprocessing import Pool
import time

# use field_names for possible options in pyshark
google_ips = ["8.8.8.8", "8.8.4.4"]
quad9_ips = ["9.9.9.9", "149.112.112.112"]
digitale_gesellschaft_ips = ["185.95.218.42", "185.95.218.43"]
appl_privacy_ips = ["37.252.185.232", "94.130.106.88", "93.177.65.183"]
cloudflare_ips = ["104.16.249.249", "104.16.248.249", "1.1.1.1", "1.0.0.1", "104.17.176.85", "104.17.175.85"]
dns_ips = []


def count_dns_https_packets(pcaps_doh):
    print("DoH starting...")
    # filter for TLS Application Data
    doh_pkts = pyshark.FileCapture(pcaps_doh, display_filter='(tls.record.content_type == 23) '
                                                             '|| (tls.record.opaque_type == 23)', use_json=True)
    pcaps_doh = pcaps_doh.split("/")[-1]
    resolver_host_name = pcaps_doh.split("--")[2]
    dns_ips = get_ips_for_resolver(resolver_host_name)
    dns_packets = [pkt for pkt in doh_pkts if pkt.ip.dst in dns_ips or pkt.ip.src in dns_ips]
    doh_pkts.close()
    with open(f"./query_stats/{names}_https_numbers.txt", "a") as f:
        f.write(f"{len(dns_packets)} {pcaps_doh} {chr(10)}")


def count_dns_tls_packets(pcaps_dot):
    print("DoT starting...")
    # filter for DNS over TLS port 853 and TLS Application data
    tls_pkts = pyshark.FileCapture(pcaps_dot, display_filter='(tcp.port == 853) && '
                                                             '((tls.record.opaque_type == 23) || '
                                                             '(tls.record.content_type == 23))', use_json=True)
    pcaps_dot = pcaps_dot.split("/")[-1]
    resolver_host_name = pcaps_dot.split("--")[2]
    dns_ips = get_ips_for_resolver(resolver_host_name)
    dns_packets = [pkt for pkt in tls_pkts if pkt.ip.dst in dns_ips or pkt.ip.src in dns_ips]
    tls_pkts.close()
    with open(f"./query_stats/{names}_tls_numbers.txt", "a") as f:
        f.write(f"{len(dns_packets)} {pcaps_dot} {chr(10)}")


def count_udp_dns_packets(pcaps_dns):
    print("DNS starting...")
    # filter for DNS over TLS port 853 and TLS Application data
    dns_pkts = pyshark.FileCapture(pcaps_dns, display_filter='dns', use_json=True)
    dns_packets = [pkt for pkt in dns_pkts]
    dns_pkts.close()
    pcaps_dns = pcaps_dns.split("/")[-1]
    with open(f"./query_stats/{names}_dns_numbers.txt", "a") as f:
        f.write(f"{len(dns_packets)} {pcaps_dns} {chr(10)}")


def get_ips_for_resolver(resolver_name):
    ret_ips = []
    if resolver_name == "dns.google":
        ret_ips = google_ips
    if resolver_name in ("one.one.one.one", "cloudflare-dns.com"):
        ret_ips = cloudflare_ips
    if resolver_name == "dns.quad9.net":
        ret_ips = quad9_ips
    if resolver_name in ("doh.applied-privacy.net", "dot1.applied-privacy.net"):
        ret_ips = appl_privacy_ips
    if resolver_name == "dns.digitale-gesellschaft.ch":
        ret_ips = digitale_gesellschaft_ips
    return ret_ips


def _get_abs_path(dir_path):
    files = os.listdir(dir_path)
    result = [dir_path + file for file in files]
    return result


def check_all_directories(root_dir):
    directories_to_check = os.listdir(root_dir)
    for elem in directories_to_check:
        path = f"{root_dir}{elem}/"
        names = path.split("/")[-2]
        files_doh_abs = _get_abs_path(f"{path}DoH/")
        files_dot_abs = _get_abs_path(f"{path}DoT/")
        with Pool(processes=4) as pool:
            pool.map(count_dns_https_packets, files_doh_abs)
            pool.map(count_dns_tls_packets, files_dot_abs)
            # pool.map(count_udp_dns_packets, files_doh_abs)


def check_directory(path):
    files_doh_abs = _get_abs_path(f"{path}DoH/")
    files_dot_abs = _get_abs_path(f"{path}DoT/")

    with Pool(processes=4) as pool:
        pool.map(count_dns_https_packets, files_doh_abs)
        pool.map(count_dns_tls_packets, files_dot_abs)


if __name__ == '__main__':
    start_time = time.time()
    dir = "files_10-05-2020--01-20-16"
    path_to_check = "/home/android-pcaps/" + dir + "/"
    names = path_to_check.split("/")[-2]
    check_directory(path_to_check)

    # root = "/home/testfiles/android-pcaps/"
    # check_all_directories(root)
    print("--- %s seconds ---" % (time.time() - start_time))
