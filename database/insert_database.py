import db
from models import Dataset, App, Trace


# create datasets for every resolver for DoH and DoT
def insert_dataset():
    with db.session_scope() as session:
        #  name, type, caching, url, ips, additional_info
        objects = [
            # closed world, no caching
            Dataset('GDOT_PN_CW', 'Google', 'dot', "PADDING", 'NO_CACHE', 'dns.google', ['8.8.8.8', '8.8.4.4'], 'closed'),
            Dataset('GDOH_PN_CW', 'Google', 'doh', "PADDING", 'NO_CACHE', 'dns.google', ['8.8.8.8', '8.8.4.4'], 'closed'),

            Dataset('CDOT_PN_CW', 'Clouflare', 'dot', "PADDING", 'NO_CACHE', 'one.one.one.one',
                    ['104.16.249.249', '104.16.248.249', '1.1.1.1', '1.0.0.1', '104.17.176.85', '104.17.175.85'],
                    'closed'),
            Dataset('CDOH_PN_CW', 'Clouflare', 'doh', "PADDING", 'NO_CACHE', 'cloudflare-dns.com',
                    ['104.16.249.249', '104.16.248.249', '1.1.1.1', '1.0.0.1', '104.17.176.85', '104.17.175.85'],
                    'closed'),

            Dataset('Q9DOT_NN_CW', 'Quad9', 'dot', "NO_PADDING", 'NO_CACHE', 'dns.quad9.net',
                    ['9.9.9.9', '149.112.112.112'], 'closed'),
            Dataset('Q9DOH_NN_CW', 'Quad9', 'doh', "NO_PADDING", 'NO_CACHE', 'dns.quad9.net',
                    ['9.9.9.9', '149.112.112.112'], 'closed'),

            Dataset('APDOT_NN_CW', 'Foundation for Applied Privacy', 'dot', "NO_PADDING", 'NO_CACHE',
                    'dot1.applied-privacy.net', ['37.252.185.232', '94.130.106.88', '93.177.65.183'], 'closed'),
            Dataset('APDOH_NN_CW', 'Foundation for Applied Privacy', 'doh', "NO_PADDING", 'NO_CACHE',
                    'doh.applied-privacy.net', ['37.252.185.232', '94.130.106.88', '93.177.65.183'], 'closed'),

            Dataset('DGDOT_NN_CW', 'Digitale Gesellschaft', 'dot', "NO_PADDING", 'NO_CACHE',
                    'dns.digitale-gesellschaft.ch', ['185.95.218.42'], 'closed'),
            Dataset('DGDOH_NN_CW', 'Digitale Gesellschaft', 'doh', "NO_PADDING", 'NO_CACHE',
                    'dns.digitale-gesellschaft.ch', ['185.95.218.42'], 'closed'),

            # closed world but caching
            Dataset('GDOT_PC_CW', 'Google', 'dot', "PADDING", 'CACHE', 'dns.google', ['8.8.8.8', '8.8.4.4'], 'closed'),
            Dataset('GDOH_PC_CW', 'Google', 'doh', "PADDING", 'CACHE', 'dns.google', ['8.8.8.8', '8.8.4.4'], 'closed'),

            Dataset('CDOT_PC_CW', 'Clouflare', 'dot', "PADDING", 'CACHE', 'one.one.one.one',
                    ['104.16.249.249', '104.16.248.249', '1.1.1.1', '1.0.0.1', '104.17.176.85', '104.17.175.85'],
                    'closed'),
            Dataset('CDOH_PC_CW', 'Clouflare', 'doh', "PADDING", 'CACHE', 'cloudflare-dns.com',
                    ['104.16.249.249', '104.16.248.249', '1.1.1.1', '1.0.0.1', '104.17.176.85', '104.17.175.85'],
                    'closed'),

            Dataset('Q9DOT_NC_CW', 'Quad9', 'dot', "NO_PADDING", 'CACHE', 'dns.quad9.net',
                    ['9.9.9.9', '149.112.112.112'], 'closed'),
            Dataset('Q9DOH_NC_CW', 'Quad9', 'doh', "NO_PADDING", 'CACHE', 'dns.quad9.net',
                    ['9.9.9.9', '149.112.112.112'], 'closed'),

            Dataset('APDOT_NC_CW', 'Foundation for Applied Privacy', 'dot', "NO_PADDING", 'CACHE',
                    'dot1.applied-privacy.net', ['37.252.185.232', '94.130.106.88', '93.177.65.183'], 'closed'),
            Dataset('APDOH_NC_CW', 'Foundation for Applied Privacy', 'doh', "NO_PADDING", 'CACHE',
                    'doh.applied-privacy.net', ['37.252.185.232', '94.130.106.88', '93.177.65.183'], 'closed'),

            Dataset('DGDOT_NC_CW', 'Digitale Gesellschaft', 'dot', "NO_PADDING", 'CACHE', 'dns.digitale-gesellschaft.ch',
                    ['185.95.218.42'], 'closed'),
            Dataset('DGDOH_NC_CW', 'Digitale Gesellschaft', 'doh', "NO_PADDING", 'CACHE', 'dns.digitale-gesellschaft.ch',
                    ['185.95.218.42'], 'closed'),
            # open world, no caching
            Dataset('GDOT_PN_OW', 'Google', 'dot', "PADDING", 'NO_CACHE', 'dns.google', ['8.8.8.8', '8.8.4.4'], 'open'),
            Dataset('GDOH_PN_OW', 'Google', 'doh', "PADDING", 'NO_CACHE', 'dns.google', ['8.8.8.8', '8.8.4.4'], 'open'),

            Dataset('CDOT_PN_OW', 'Clouflare', 'dot', "PADDING", 'NO_CACHE', 'one.one.one.one',
                    ['104.16.249.249', '104.16.248.249', '1.1.1.1', '1.0.0.1', '104.17.176.85', '104.17.175.85'],
                    'open'),
            Dataset('CDOH_PN_OW', 'Clouflare', 'doh', "PADDING", 'NO_CACHE', 'cloudflare-dns.com',
                    ['104.16.249.249', '104.16.248.249', '1.1.1.1', '1.0.0.1', '104.17.176.85', '104.17.175.85'],
                    'open'),

            Dataset('Q9DOT_NN_OW', 'Quad9', 'dot', "NO_PADDING", 'NO_CACHE', 'dns.quad9.net',
                    ['9.9.9.9', '149.112.112.112'], 'open'),
            Dataset('Q9DOH_NN_OW', 'Quad9', 'doh', "NO_PADDING", 'NO_CACHE', 'dns.quad9.net',
                    ['9.9.9.9', '149.112.112.112'], 'open'),

            Dataset('APDOT_NN_OW', 'Foundation for Applied Privacy', 'dot', "NO_PADDING", 'NO_CACHE',
                    'dot1.applied-privacy.net', ['37.252.185.232', '94.130.106.88', '93.177.65.183'], 'open'),
            Dataset('APDOH_NN_OW', 'Foundation for Applied Privacy', 'doh', "NO_PADDING", 'NO_CACHE',
                    'doh.applied-privacy.net', ['37.252.185.232', '94.130.106.88', '93.177.65.183'], 'open'),

            Dataset('DGDOT_NN_OW', 'Digitale Gesellschaft', 'dot', "NO_PADDING", 'NO_CACHE',
                    'dns.digitale-gesellschaft.ch', ['185.95.218.42'], 'open'),
            Dataset('DGDOH_NN_OW', 'Digitale Gesellschaft', 'doh', "NO_PADDING", 'NO_CACHE',
                    'dns.digitale-gesellschaft.ch', ['185.95.218.42'], 'open'),

            # open world, caching
            Dataset('GDOT_PC_OW', 'Google', 'dot', "PADDING", 'CACHE', 'dns.google', ['8.8.8.8', '8.8.4.4'], 'open'),
            Dataset('GDOH_PC_OW', 'Google', 'doh', "PADDING", 'CACHE', 'dns.google', ['8.8.8.8', '8.8.4.4'], 'open'),

            Dataset('CDOT_PC_OW', 'Clouflare', 'dot', "PADDING", 'CACHE', 'one.one.one.one',
                    ['104.16.249.249', '104.16.248.249', '1.1.1.1', '1.0.0.1', '104.17.176.85', '104.17.175.85'],
                    'open'),
            Dataset('CDOH_PC_OW', 'Clouflare', 'doh', "PADDING", 'CACHE', 'cloudflare-dns.com',
                    ['104.16.249.249', '104.16.248.249', '1.1.1.1', '1.0.0.1', '104.17.176.85', '104.17.175.85'],
                    'open'),

            Dataset('Q9DOT_NC_OW', 'Quad9', 'dot', "NO_PADDING", 'CACHE', 'dns.quad9.net',
                    ['9.9.9.9', '149.112.112.112'], 'open'),
            Dataset('Q9DOH_NC_OW', 'Quad9', 'doh', "NO_PADDING", 'CACHE', 'dns.quad9.net',
                    ['9.9.9.9', '149.112.112.112'], 'open'),

            Dataset('APDOT_NC_OW', 'Foundation for Applied Privacy', 'dot', "NO_PADDING", 'CACHE',
                    'dot1.applied-privacy.net', ['37.252.185.232', '94.130.106.88', '93.177.65.183'], 'open'),
            Dataset('APDOH_NC_OW', 'Foundation for Applied Privacy', 'doh', "NO_PADDING", 'CACHE',
                    'doh.applied-privacy.net', ['37.252.185.232', '94.130.106.88', '93.177.65.183'], 'open'),

            Dataset('DGDOT_NC_OW', 'Digitale Gesellschaft', 'dot', "NO_PADDING", 'CACHE',
                    'dns.digitale-gesellschaft.ch', ['185.95.218.42'], 'open'),
            Dataset('DGDOH_NC_OW', 'Digitale Gesellschaft', 'doh', "NO_PADDING", 'CACHE',
                    'dns.digitale-gesellschaft.ch', ['185.95.218.42'], 'open'),
        ]
        session.bulk_save_objects(objects)


# assign each dataset the list of apps
# note that the list of apps might differ for datasets
def insert_apps():
    with db.session_scope() as session:
        objects = []
        with open('../phone/apps/packages.txt', 'r', encoding='utf-8') as file:
            packages = file.read().splitlines()
        q = session.query(Dataset.id).filter(Dataset.id <= 20)
        for id in q:
            for pkg in packages:
                objects.append(App(pkg, id))
        with open('../phone/apps/packages_ow.txt', 'r', encoding='utf-8') as file:
            packages_ow = file.read().splitlines()
        q = session.query(Dataset.id).filter(Dataset.id > 20)
        for id in q:
            for pkg in packages_ow:
                objects.append(App(pkg, id))
        session.bulk_save_objects(objects)


if __name__ == '__main__':
    insert_dataset()
    insert_apps()
