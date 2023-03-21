# -*- coding: utf-8 -*-
from src.common import registry, BColors
from tabulate import tabulate
import sys
import getopt
import tqdm
import json

__VERSION__ = "0.1"
__DESC__ = "Utility for outdated packages automatic detection"
__AUTHOR__ = "ksot1k"
__URL__ = "https://github.com/ksotik/upddetect"
__LOGO__ = """
                                                            ___                           ___     
              ,-.----.        ,---,      ,---,            ,--.'|_                       ,--.'|_   
         ,--, \    /  \     ,---.'|    ,---.'|            |  | :,'                      |  | :,'  
       ,'_ /| |   :    |    |   | :    |   | :            :  : ' :                      :  : ' :  
  .--. |  | : |   | .\ :    |   | |    |   | |   ,---.  .;__,'  /     ,---.     ,---. .;__,'  /   
,'_ /| :  . | .   : |: |  ,--.__| |  ,--.__| |  /     \ |  |   |     /     \   /     \|  |   |    
|  ' | |  . . |   |  \ : /   ,'   | /   ,'   | /    /  |:__,'| :    /    /  | /    / ':__,'| :    
|  | ' |  | | |   : .  |.   '  /  |.   '  /  |.    ' / |  '  : |__ .    ' / |.    ' /   '  : |__  
:  | : ;  ; | :     |`-''   ; |:  |'   ; |:  |'   ;   /|  |  | '.'|'   ;   /|'   ; :__  |  | '.'| 
'  :  `--'   \:   : :   |   | '/  '|   | '/  ''   |  / |  ;  :    ;'   |  / |'   | '.'| ;  :    ; 
:  ,      .-./|   | :   |   :    :||   :    :||   :    |  |  ,   / |   :    ||   :    : |  ,   /  
 `--`----'    `---'.|    \   \  /   \   \  /   \   \  /    ---`-'   \   \  /  \   \  /   ---`-'   
                `---`     `----'     `----'     `----'               `----'    `----'             
"""

__HELP__ = BColors.BOLD + "usage: upddetect [options]" + BColors.ENDC + """
Options:
-s: detect only security updates
-d: detect only dist updates
-a: detect all updates
-j: work silently, display json when finished
-v: show version"""

from src.packet_managers.general import PacketManager


def print_welcome():
    print(BColors.OKCYAN + __LOGO__ + BColors.ENDC)
    print()
    print(__DESC__)
    print("Version: %s" % __VERSION__)
    print("Author: %s" % __AUTHOR__)
    print("Repository: %s" % (BColors.UNDERLINE + __URL__ + BColors.ENDC))
    print()


def main(argv):
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
                    all_updates = list(set(updates1 + updates2))
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
    main(sys.argv[1:])
