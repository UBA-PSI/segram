import pyshark
import os
from multiprocessing import Pool
import time
import datetime
import numpy as np
import db
from models import Dataset, App, Trace, Packet, Features

google_ips = ["8.8.8.8", "8.8.4.4"]
quad9_ips = ["9.9.9.9", "149.112.112.112"]
digitale_gesellschaft_ips = ["185.95.218.42", "185.95.218.43"]
appl_privacy_ips = ["37.252.185.232", "94.130.106.88", "93.177.65.183"]
cloudflare_ips = ["104.16.249.249", "104.16.248.249", "1.1.1.1", "1.0.0.1", "104.17.176.85", "104.17.175.85"]

packet_objects = []
trace_objects = []
feature_objects = []


def get_app_id_dataset(my_session, protocol, resolver_name, application):
    # get the database id based on hostname and type
    q = my_session.query(Dataset.id).filter(Dataset.dns_type == protocol, Dataset.hostname == resolver_name,
                                            Dataset.caching == "CACHE", Dataset.world == "open")
    database_id = 0
    app_id = 0
    for row in q:
        database_id = row.id
        # print(database_id)
    # get the app_id based on dataset and app name
    qtwo = my_session.query(App).join(Dataset, Dataset.id == App.dataset_id).filter(application == App.name,
                                                                                    database_id == App.dataset_id)
    for rowt in qtwo:
        app_id = rowt.id
    return app_id


def insert_packets(pkt_session, trace, pcap_packets, entry, data, datetime_trace):
    # insert packets
    dns_ips = get_ips_for_resolver(entry[2])
    dns_packets = [pkt for pkt in pcap_packets if pkt.ip.dst in dns_ips or pkt.ip.src in dns_ips]
    tls_record_size_dns_packets = []
    tls_record_size_dns_req = []
    tls_record_size_dns_resp = []
    time_epochs_tls_sizes = []
    pkt_w_mult_tls_records_in_trace = 0
    if len(dns_packets) > 0:
        time_previous_packet = float(dns_packets[0].frame_info.time_epoch)
    for pkt in dns_packets:
        # store time between the TLS packets
        time_epoch = (datetime.datetime.fromtimestamp(float(pkt.frame_info.time_epoch)) -
                      datetime.datetime.fromtimestamp(time_previous_packet)).total_seconds()
        time_previous_packet = float(pkt.frame_info.time_epoch)
        packet_nr = pkt.number
        packet_len = len(pkt)
        record_lens = []
        if isinstance(pkt.tls.record, list):
            for rec in pkt.tls.record:
                try:
                    if rec.content_type == str(23):
                        record_lens.append(int(rec.record.length))
                except AttributeError:
                    print(f"{data} --- TLS Record List has no Content Type 23")
                try:
                    if rec.opaque_type == str(23):
                        record_lens.append(int(rec.length))
                except AttributeError:
                    print(f"{data} --- TLS Record List has no Opaque Type 23")
            tls_record_len = sum(record_lens)
            if tls_record_len > 0:
                pkt_w_mult_tls_records_in_trace += 1
        else:
            tls_record_len = int(pkt.tls.record.length)
        if pkt.ip.dst in dns_ips:
            direction = "request"
            tls_record_len = tls_record_len * -1
            tls_record_size_dns_req.append(tls_record_len)
            tls_record_size_dns_packets.append(tls_record_len)
            record_lens = [-1 * entry for entry in record_lens]
            packet_len = packet_len * -1
        if pkt.ip.src in dns_ips:
            direction = "response"
            tls_record_size_dns_resp.append(int(tls_record_len))
            tls_record_size_dns_packets.append(int(tls_record_len))
        time_epochs_tls_sizes.append(time_epoch)
        pkt_session.add(Packet(trace, packet_nr, packet_len, tls_record_len, direction, record_lens, time_epoch))

    # add feature table
    app_name = entry[-1].replace(".pcap", "")
    features = Features(trace, datetime_trace, app_name,
                        len(dns_packets), len(tls_record_size_dns_req), len(tls_record_size_dns_resp),
                        tls_record_size_dns_packets, tls_record_size_dns_req, tls_record_size_dns_resp,
                        np.mean(tls_record_size_dns_packets), np.mean(tls_record_size_dns_req),
                        np.mean(tls_record_size_dns_resp), np.std(tls_record_size_dns_packets),
                        np.std(tls_record_size_dns_req), np.std(tls_record_size_dns_resp),
                        np.median(tls_record_size_dns_packets), np.median(tls_record_size_dns_req),
                        np.median(tls_record_size_dns_resp), time_epochs_tls_sizes, pkt_w_mult_tls_records_in_trace)
    pkt_session.add(features)


def insert_traces(path, packets, pcap_type):
    time_resolver_app = path.split("/")[-1]
    entries = time_resolver_app.split("--")
    date = entries[0].split("-")

    timestamp = f'{date[-1]}-{date[1]}-{date[0]} {entries[1].replace("-", ":")}'
    app_name = entries[-1].replace(".pcap", "")
    resolver_hostname = entries[2]
    timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    with db.session_scope() as session:
        app_id = get_app_id_dataset(session, pcap_type, resolver_hostname, app_name)
        # insert trace
        trace = Trace(timestamp, app_id)
        session.add(trace)
        session.flush()
        trace_id = trace.id
        insert_packets(session, trace_id, packets, entries, time_resolver_app, timestamp)


def calc_features_dns_https_packets(pcaps_doh):
    print("DoH starting...")
    # filter for TLS Application Data
    doh_pkts = pyshark.FileCapture(pcaps_doh, display_filter='(tls.record.content_type == 23) '
                                                             '|| (tls.record.opaque_type == 23)', use_json=True)

    insert_traces(pcaps_doh, doh_pkts, "doh")

    doh_pkts.close()


def calc_features_dns_tls_packets(pcaps_dot):
    print("DoT starting...")
    # filter for DNS over TLS port 853 and TLS Application data
    tls_pkts = pyshark.FileCapture(pcaps_dot, display_filter='(tcp.port == 853) && '
                                                             '((tls.record.opaque_type == 23) || '
                                                             '(tls.record.content_type == 23))', use_json=True)
    insert_traces(pcaps_dot, tls_pkts, "dot")

    tls_pkts.close()


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


def check_directory(path):
    files_doh_abs = _get_abs_path(f"{path}DoH/")
    files_dot_abs = _get_abs_path(f"{path}DoT/")
    with Pool(processes=4) as pool:
        pool.map(calc_features_dns_https_packets, files_doh_abs)
        pool.map(calc_features_dns_tls_packets, files_dot_abs)


def check_all_directories(root_dir):
    directories_in_dir = os.listdir(root_dir)
    directories_to_check = [single_dir for single_dir in directories_in_dir if "files_" in single_dir]
    for elem in directories_to_check:
        path = f"{root_dir}{elem}/"
        files_doh_abs = _get_abs_path(f"{path}DoH/")
        files_dot_abs = _get_abs_path(f"{path}DoT/")
        with Pool(processes=4) as pool:
            pool.map(calc_features_dns_https_packets, files_doh_abs)
            pool.map(calc_features_dns_tls_packets, files_dot_abs)


if __name__ == '__main__':
    start_time = time.time()
    # path to pcap files
    root = "/home/user/path/to/pcaps/"
    # write all PCAPS in all sub-directories to the database
    for pcap_dir in root:
        check_all_directories(root + pcap_dir)

    # Alternative: write only a single directory to the database
    # dir = "files_28-05-2020--04-25-15"
    # path_to_check = root + dir + "/"
    # check_directory(path_to_check)
    print("--- %s seconds ---" % (time.time() - start_time))
