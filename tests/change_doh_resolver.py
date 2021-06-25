from time import sleep
import sys
sys.path.insert(0, '../phone')
import DoH_Manager

if __name__ == '__main__':
    intra = DoH_Manager.Intra()
    for resolver_name in intra.resolver:
        sleep(1)
        intra.change_resolver(resolver_name)
        sleep(1)
        intra.enable_intra()
        sleep(1)
        intra.disable_intra()
    intra.force_stop_intra()