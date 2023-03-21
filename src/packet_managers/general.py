# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from src.variables import BColors
import os
import subprocess
import sys


class PacketManager(ABC):
    colorize = False
    pm_path = ""

    def __init__(self, instance_path: str = "", colorize: bool = True):
        self.pm_path = instance_path
        self.colorize = colorize

    @abstractmethod
    def __repr__(self) -> str:
        return "Abstract Packet Manager"

    @staticmethod
    def get_human_name() -> str:
        return "Abstract Packet Manager"

    @staticmethod
    def get_type() -> str:
        return "abstract_packet_manager"

    @staticmethod
    def which(s: str) -> str:
        p = subprocess.run(['/usr/bin/which', s], stdout=subprocess.PIPE)
        return p.stdout.decode('utf-8').strip()

    def is_available(self) -> bool:
        if self.pm_path:
            if not os.path.isfile(self.pm_path):
                self.print_error("%s is not a file or not exists" % self.pm_path)
                return False
            if not os.access(self.pm_path, os.X_OK):
                self.print_error("%s is not executable" % self.pm_path)
                return False
            return True

    def detect_updates(self, only_security: bool = False) -> (str, list):
        return None, []

    def detect_dist_updates(self, only_security: bool = False) -> (str, list):
        return None, []

    def find_all_instances(self) -> list:
        return []

    @staticmethod
    def make_result_line(package: str, curr_ver: str, rec_ver: str, desc: str = "", colorize: bool = True) -> dict:
        return {
            'package': package,
            'current': BColors.FAIL + curr_ver + BColors.ENDC if colorize else curr_ver,
            'recommended': BColors.BOLD + BColors.WARNING + rec_ver + BColors.ENDC if colorize else rec_ver,
            'description': desc
        }

    def print_error(self, msg: str):
        if self.colorize:
            print("", file=sys.stderr)
            print("Some error occurred, but we are continue to work:", file=sys.stderr)
            print(BColors.FAIL + msg.strip() + BColors.ENDC, file=sys.stderr)
        else:
            print(msg, file=sys.stderr)
