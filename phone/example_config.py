# caching could either be ENABLED OR DISABLED
CACHING = 'ENABLED'
# Remote Directory where the directories for each round are stored
SAVE_DIR = '/home/android-pcaps/'
# Path to the list of apps which should be started
APPS = './apps/packages_ow.txt'
# Hostname of the remote host, which captures the traffic as specified in the ssh config file
SSH_HOST = 'capturebox'
# time to wait before closing the application after launching
CAPTURE_TIME = 20

# use cross platform DoH implementation (DOH_IMPL != 'pixel') or one specifically designed for Pixel 3aXL resolution
DOH_IMPL = "pixel"

# list of DoH resolvers
DOH_RESOLVER = ['https://dns.google/dns-query', 'https://cloudflare-dns.com/dns-query',
                'https://dns.quad9.net/dns-query', 'https://doh.applied-privacy.net/query',
                'https://dns.digitale-gesellschaft.ch/dns-query']

# list of DoT resolvers
DOT_RESOLVER = [("dns.google", "8.8.8.8"), ("one.one.one.one", "1.1.1.1"), ("dns.quad9.net", "9.9.9.9"),
                ("dot1.applied-privacy.net", "94.130.106.88"), ("dns.digitale-gesellschaft.ch", "185.95.218.42")]

# List of apps to deinstall called by package_manager.py
DEL_APPS = './apps/pkg_del.txt'
