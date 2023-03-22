# -*- coding: utf-8 -*-
from upddetect.common import registry
from tabulate import tabulate
from upddetect.packet_managers.general import PacketManager
from upddetect.variables import BColors, __DESC__, __URL__, __AUTHOR__, __VERSION__, __LOGO__, __HELP__
import sys
import getopt
import tqdm
import json


def print_welcome():
    print(BColors.OKCYAN + __LOGO__ + BColors.ENDC)
    print()
    print(__DESC__)
    print("Version: %s" % __VERSION__)
    print("Author: %s" % __AUTHOR__)
    print("Repository: %s" % (BColors.UNDERLINE + __URL__ + BColors.ENDC))
    print()


def main():
    argv = sys.argv[1:]

    only_security = dist_updates = all_updates = json_output = False
    updates1 = updates2 = []
    opts, args = getopt.getopt(argv, "hvsdaj")
    for opt, arg in opts:
        if opt == "-h":
            print_welcome()
            print(__HELP__)
            sys.exit()
        elif opt == "-v":
            print("upddetect {}".format(__VERSION__))
            sys.exit()
        elif opt == "-s":
            only_security = True
        elif opt == "-d":
            dist_updates = True
        elif opt == "-a":
            all_updates = True
        elif opt == "-j":
            json_output = True

    if not json_output:
        print_welcome()

        if only_security or dist_updates:
            print(BColors.OKCYAN + BColors.BOLD + "You selected '%s updates' only mode, be carefully because it "
                                                  "could skip another updates" %
                  ("security" if only_security else "dist") + BColors.ENDC)
            print()

        print(BColors.HEADER + "Supported packet managers:" + BColors.ENDC)
        for cls in registry.packet_managers:
            print(BColors.OKBLUE + "* " + cls.get_human_name() + BColors.ENDC)

    if not json_output:
        print()
        print(BColors.HEADER + "Scan outdated packages:" + BColors.ENDC)
    packages = []
    for cls in registry.packet_managers:
        pm_root = cls(colorize=not json_output)
        pm_instances = pm_root.find_all_instances()

        progress = tqdm.tqdm(pm_instances, ascii=True, disable=json_output)
        for pm in progress:
            if pm.is_available():
                progress.set_description("%s" % pm)
                if not dist_updates or all_updates:
                    p, updates1 = pm.detect_updates(only_security)
                if dist_updates or all_updates:
                    p, updates2 = pm.detect_dist_updates(only_security)
                if all_updates:
                    all_updates = updates1 + updates2
                    packages.append({
                        'pm': str(pm),
                        'type': pm.get_type(),
                        'packages': all_updates
                    })
                elif dist_updates:
                    packages.append({
                        'pm': str(pm),
                        'type': pm.get_type(),
                        'packages': updates2
                    })
                else:
                    packages.append({
                        'pm': str(pm),
                        'type': pm.get_type(),
                        'packages': updates1
                    })
                progress.set_description("done")

    if not json_output:
        print()
        print(BColors.HEADER + "Founded:" + BColors.ENDC)
        print()
        for package in packages:
            if not package['packages']:
                print(BColors.OKGREEN + package['pm'] + BColors.ENDC)
                print("everything is up to date, but of course you need to check it manually to be sure")
                print()
                continue
            else:
                print(BColors.WARNING + package['pm'] + BColors.ENDC)
            print(tabulate(package['packages'],
                           headers=PacketManager.make_result_line(
                               "package", "current", "recommended", "description", False),
                           missingval=""))
            print()
    else:
        print(json.dumps(packages))


if __name__ == "__main__":
    main()
