import subprocess
from time import sleep
from datetime import datetime
import DoH_Manager, DoT_Manager, capture, DoH_Manager_CP

tld = 'wordpress.com'
doh_resolver = ['https://dns.adguard.com/dns-query', 'https://dns.google/dns-query',
                'https://cloudflare-dns.com/dns-query', 'https://mozilla.cloudflare-dns.com/dns-query',
                'https://security.cloudflare-dns.com/dns-query', 'https://family.cloudflare-dns.com/dns-query',
                'https://dns.quad9.net/dns-query', 'https://dns9.quad9.net/dns-query',
                'https://dns10.quad9.net/dns-query', 'https://dns11.quad9.net/dns-query',
                'https://doh.opendns.com/dns-query', 'https://doh.familyshield.opendns.com/dns-query',
                'https://doh.cleanbrowsing.org/doh/family-filter/', 'https://doh.xfinity.com/dns-query',
                'https://dohdot.coxlab.net/dns-query', 'https://odvr.nic.cz/doh', 'https://doh.dnslify.com/dns-query',
                'https://dns.nextdns.io/', 'https://dns.dnsoverhttps.net/dns-query', 'https://doh.crypto.sx/dns-query',
                'https://doh.powerdns.org/', 'https://doh-fi.blahdns.com/dns-query',
                'https://doh-jp.blahdns.com/dns-query', 'https://doh-de.blahdns.com/dns-query',
                'https://doh.ffmuc.net/dns-query', 'https://dns.dns-over-https.com/dns-query',
                'https://dns.rubyfish.cn/dns-query', 'https://dns.containerpi.com/dns-query',
                'https://dns.containerpi.com/doh/family-filter/', 'https://dns.containerpi.com/doh/secure-filter/',
                'https://doh-2.seby.io/dns-query', 'https://dns-nyc.aaflalo.me/dns-query',
                'https://dns.aaflalo.me/dns-query', 'https://doh.applied-privacy.net/query',
                'https://doh.captnemo.in/dns-query',
                'https://doh.tiar.app/dns-query', 'https://doh.tiarap.org/dns-query', 'https://doh.dns.sb/dns-query',
                'https://rdns.faelix.net/', 'https://doh.li/dns-query', 'https://doh.armadillodns.net/dns-query',
                'https://jp.tiar.app/dns-query', 'https://jp.tiarap.org/dns-query', 'https://doh.42l.fr/dns-query',
                'https://dns.hostux.net/dns-query', 'https://dns.hostux.net/ads', 'https://dns.aa.net.uk/dns-query',
                'https://adblock.mydns.network/dns-query', 'https://ibksturm.synology.me/dns-query',
                'https://jcdns.fun/dns-query', 'https://ibuki.cgnat.net/dns-query', 'https://dns.twnic.tw/dns-query',
                'https://example.doh.blockerdns.com/dns-query', 'https://dns.digitale-gesellschaft.ch/dns-query',
                'https://doh.libredns.gr/dns-query', 'https://doh.centraleu.pi-dns.com/dns-query',
                'https://doh.northeu.pi-dns.com/dns-query', 'https://doh.westus.pi-dns.com/dns-query',
                'https://doh.eastus.pi-dns.com/dns-query', 'https://dns.flatuslifir.is/dns-query',
                'https://private.canadianshield.cira.ca/dns-query',
                'https://protected.canadianshield.cira.ca/dns-query',
                'https://family.canadianshield.cira.ca/dns-query', 'https://ordns.he.net/dns-query',
                'https://dns.switch.ch/dns-query', 'https://dnsforge.de/dns-query',
                'https://fi.doh.dns.snopyta.org/dns-query', 'https://resolver-eu.lelux.fi/dns-query',
                'https://dns.dnshome.de/dns-query', 'https://dns.nextdns.io/4a635c']

dot_resolver = ['dot.xfinity.com', 'security-filter-dns.cleanbrowsing.org', 'dns.adguard.com', 'dnsovertls.sinodun.com',
                'dnsovertls1.sinodun.com', 'getdnsapi.net', 'unicast.censurfridns.dk', 'kaitain.restena.lu',
                'dns.cmrg.net', 'dnsovertls3.sinodun.com', 'dnsovertls2.sinodun.com', 'ns1.dnsprivacy.at',
                'dns.neutopia.org', 'dot-jp.blahdns.com', 'dot-de.blahdns.com',
                'privacydns.go6lab.si', 'dns.oszx.co',
                'ibksturm.synology.me', 'dnsotls.lab.nic.cl', 'dns.rubyfish.cn', 'dot.libredns.gr', 'odvr.nic.cz',
                '4a635c.dns.nextdns.io']


def clear_dns_cache():
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


def check_doh_padding():
    intra = DoH_Manager_CP.Intra()
    for resolver_name in doh_resolver:
        clear_dns_cache()
        intra.change_resolver(resolver_name)
        resolver = resolver_name.split('/')[2]
        sleep(1)
        path_to_save = f"/home/padding/DoH/{resolver}.pcap"
        cmd = f"tcpdump -i wlp5s0 -w {path_to_save}"
        subprocess.Popen(["ssh", "capturebox", cmd])
        sleep(1)
        intra.enable_intra()
        if not intra.get_status():
            print(f"---------had to correct intra at {datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}---------")
            intra.enable_intra()
            sleep(3)
        print(f"Querying {resolver}")
        sleep(3)
        for i in range(100):
            query_url = tld
            if 63 > i > 0:
                query_url = str("a" * i) + "." + tld
            if 124 > i > 62:
                query_url = str("a" * (i % 62)) + "." + str("a" * 62) + "." + tld
            if 187 > i > 124:
                query_url = str("a" * (i % 124)) + "." + str("a" * 62) + "." + str("a" * 62) + "." + tld
            print(query_url)
            sleep(1)
            resp = subprocess.run(["adb", "shell", "ping -c 1", query_url], capture_output=True,
                                  universal_newlines=True)
            print(resp)
        sleep(2)
        cmd = f"killall tcpdump"
        subprocess.Popen(["ssh", "capturebox", cmd])
        print("saved file for " + resolver)
        intra.disable_intra()
        sleep(120)


def check_dot_padding():
    dot_manager = DoT_Manager.DoT_Manager()
    dot_manager.enable_private_dns()
    for resolver_name in dot_resolver:
        clear_dns_cache()
        dot_manager.change_resolver(resolver_name)
        sleep(1)
        print(f"Querying {resolver_name}")
        path_to_save = f"/home/padding/DoT/{resolver_name}.pcap"
        cmd = f"tcpdump -i wlp5s0 -w {path_to_save}"
        subprocess.Popen(["ssh", "capturebox", cmd])
        sleep(3)
        for i in range(100):
            query_url = tld
            if 63 > i > 0:
                query_url = str("a" * i) + "." + tld
            if 124 > i > 62:
                query_url = str("a" * (i % 62)) + "." + str("a" * 62) + "." + tld
            if 187 > i > 124:
                query_url = str("a" * (i % 124)) + "." + str("a" * 62) + "." + str("a" * 62) + "." + tld
            sleep(1)
            resp = subprocess.run(["adb", "shell", "ping -c 1", query_url], capture_output=True,
                                  universal_newlines=True)
            print(resp)
        sleep(2)
        cmd = f"killall tcpdump"
        subprocess.Popen(["ssh", "capturebox", cmd])
        print("saved file " + resolver_name)
        sleep(120)
    dot_manager.disable_private_dns()


def check_udp_dns():
    print(f"Querying DNS Resolver")
    path_to_save = f"/home/padding/udp.pcap"
    cmd = f"tcpdump -i wlp5s0 -w {path_to_save}"
    subprocess.Popen(["ssh", "capturebox", cmd])
    sleep(3)
    for i in range(187):
        query_url = tld
        if 63 > i > 0:
            query_url = str("a" * i) + "." + tld
        if 124 > i > 62:
            query_url = str("a" * (i % 62)) + "." + str("a" * 62) + "." + tld
        if 187 > i > 124:
            query_url = str("a" * (i % 124)) + "." + str("a" * 62) + "." + str("a" * 62) + "." + tld
        sleep(1)
        resp = subprocess.run(["adb", "shell", "ping -c 1", query_url], capture_output=True,
                              universal_newlines=True)
        print(resp)
    sleep(2)
    cmd = f"killall tcpdump"
    subprocess.Popen(["ssh", "capturebox", cmd])
    print("saved file")


if __name__ == '__main__':
    # check_udp_dns()
    check_dot_padding()
    check_doh_padding()
