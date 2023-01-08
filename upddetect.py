# -*- coding: utf-8 -*-
import sys
import getopt
from src.common import registry

__VERSION__ = "0.1"


def main(argv):
    opts, args = getopt.getopt(argv, "hv")
    for opt, arg in opts:
        if opt == '-h':
            print('upddetect')
            sys.exit()
        elif opt == '-v':
            print('upddetect version {}'.format(__VERSION__))
            sys.exit()

    for cls in registry.packet_managers:
        pm = cls()
        print(pm)
        if pm.is_available():
            updates = pm.detect_updates()
            print(updates)


if __name__ == "__main__":
    main(sys.argv[1:])
