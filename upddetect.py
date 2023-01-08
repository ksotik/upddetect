# -*- coding: utf-8 -*-
import sys
import getopt
from src.common import registry

__VERSION__ = "0.1"

def print_list(lst: list, prefix: str) -> None:
    for i in lst:
        print('{}: {}'.format(prefix, i))


def main(argv):
    only_security = dist_updates = all_updates = False
    opts, args = getopt.getopt(argv, "hvsda")
    for opt, arg in opts:
        if opt == '-h':
            print('upddetect')
            sys.exit()
        elif opt == '-v':
            print('upddetect version {}'.format(__VERSION__))
            sys.exit()
        elif opt == '-s':
            only_security = True
        elif opt == '-d':
            dist_updates = True
        elif opt == '-a':
            all_updates = True

    for cls in registry.packet_managers:
        pm = cls()
        if pm.is_available():
            if not dist_updates or all_updates:
                updates = pm.detect_updates(only_security)
            if dist_updates or all_updates:
                dist_updates = pm.detect_dist_updates(only_security)
            if all_updates:
                all_updates = list(set(updates + dist_updates))
                print_list(all_updates, pm)
            elif dist_updates:
                print_list(dist_updates, pm)
            else:
                print_list(updates, pm)


if __name__ == "__main__":
    main(sys.argv[1:])
