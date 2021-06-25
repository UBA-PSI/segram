import pyshark
import os
from collections import Counter


def check_doh(path_doh):
    pcaps_doh = sorted(os.listdir(path_doh))
    print(pcaps_doh)
    padded_resolvers = []
    unpadded_resolvers = []
    for file in pcaps_doh:
        list_of_doh_ips = []
        dns = pyshark.FileCapture(path_doh + file, display_filter='dns')
        for pkt in dns:
            hostname = file.replace(".pcap", "")
            if pkt.dns.flags == "0x00008180" and pkt.dns.qry_type == "1" and pkt.dns.resp_name == hostname:
                print("File:", hostname)
                try:
                    dns_ips = pkt.dns.a.all_fields
                    for i in range(len(dns_ips)):
                        list_of_doh_ips.append(dns_ips[i].show)
                except:
                    pass
        dns.close()
        enc_dns = pyshark.FileCapture(path_doh + file, display_filter='(tls.record.content_type == 23) ||'
                                       '(tls.record.opaque_type == 23)', use_json=True)
        doh_pkt_lengths = []
        if hostname == 'cloudflare-dns.com':
            list_of_doh_ips.extend(["1.1.1.1", "1.0.0.1"])
        print(list_of_doh_ips)
        for pkt in enc_dns:
            if pkt.ip.src in list_of_doh_ips:
                record_lens = []
                if isinstance(pkt.tls.record, list):
                    for rec in pkt.tls.record:
                        try:
                            if rec.content_type == str(23):
                                record_lens.append(int(rec.record.length))
                        except AttributeError:
                            pass
                        try:
                            if rec.opaque_type == str(23):
                                record_lens.append(int(rec.length))
                        except AttributeError:
                            pass
                    doh_pkt_lengths.append(sum(record_lens))
                else:
                    doh_pkt_lengths.append(pkt.tls.record.length)
        enc_dns.close()
        print("Summe:", sum(Counter(doh_pkt_lengths).values()))
        print("Anzahl:", len(Counter(doh_pkt_lengths)))
        if len(Counter(doh_pkt_lengths)) > 20:
            unpadded_resolvers.append(hostname)
        elif 0 < len(Counter(doh_pkt_lengths)) < 20:
            padded_resolvers.append(hostname)
        print("\n")
    print(padded_resolvers)


def check_dot(path_dot):
    pcaps_dot = sorted(os.listdir(path_dot))
    padded_resolvers = []
    unpadded_resolvers = []
    for file in pcaps_dot:
        print(file)
        hostname = file.replace(".pcap", "")
        enc_dns = pyshark.FileCapture(path_dot + file, display_filter='(tcp.port == 853) && '
                                                                      '((tls.record.opaque_type == 23) || '
                                                                      '(tls.record.content_type == 23))', use_json=True)
        dot_pkt_lengths = []
        for pkt in enc_dns:
            record_lens = []
            if isinstance(pkt.tls.record, list):
                for rec in pkt.tls.record:
                    try:
                        if rec.content_type == str(23):
                            record_lens.append(int(rec.record.length))
                    except AttributeError:
                        pass
                    try:
                        if rec.opaque_type == str(23):
                            record_lens.append(int(rec.length))
                    except AttributeError:
                        pass
                dot_pkt_lengths.append(sum(record_lens))
            else:
                dot_pkt_lengths.append(pkt.tls.record.length)
        enc_dns.close()
        print(Counter(dot_pkt_lengths))
        print("Summe:", sum(Counter(dot_pkt_lengths).values()))
        print("Anzahl:", len(Counter(dot_pkt_lengths)))
        if len(Counter(dot_pkt_lengths)) > 20:
            unpadded_resolvers.append(hostname)
        elif 0 < len(Counter(dot_pkt_lengths)) < 20:
            padded_resolvers.append(hostname)
        print("\n")
    print(padded_resolvers)


if __name__ == '__main__':
    path_doh = "/home/android-pcaps/padding/padding_more/DoH/"
    check_doh(path_doh)
    path_dot = "/home/android-pcaps/padding/padding_more/DoT/"
    check_dot(path_dot)
