# -*- coding: utf-8 -*-
import sys
import getopt
from src.common import registry

__VERSION__ = "0.1"


def print_list(lst: list, prefix: str) -> None:
    for i in lst:
        print('{}'.format(i))


def main(argv):
    only_security = dist_updates = all_updates = False
    updates1 = updates2 = []
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
        pm_root = cls()
        pm_instances = pm_root.find_all_instances()
        for pm in pm_instances:
            if pm.is_available():
                if not dist_updates or all_updates:
                    p, updates1 = pm.detect_updates(only_security)
                if dist_updates or all_updates:
                    p, updates2 = pm.detect_dist_updates(only_security)
                if all_updates:
                    all_updates = list(set(updates1 + updates2))
                    print("%s: %s:" % (pm, p))
                    print_list(all_updates, pm)
                elif dist_updates:
                    print("%s: %s:" % (pm, p))
                    print_list(updates2, pm)
                else:
                    print("%s: %s:" % (pm, p))
                    print_list(updates1, pm)

# TODO: добавить опцию, при установке которой upddetect будет пытаться доставить недостающий софт (например safety в каждое pip окружение)


if __name__ == "__main__":
    main(sys.argv[1:])
