# -*- coding: utf-8 -*-
from .general import PacketManager
from upddetect.common import registry
import subprocess


class AptPacketManager(PacketManager):

    def __repr__(self) -> str:
        return self.pm_path if self.pm_path else "APT"

    @staticmethod
    def get_human_name() -> str:
        return "APT (apt-get, apt)"

    @staticmethod
    def get_type() -> str:
        return "apt"

    def is_available(self) -> bool:
        if PacketManager.is_available(self):
            return True

        self.pm_path = self.which('apt-get')
        if not self.pm_path:
            self.pm_path = self.which('apt')

        if self.pm_path:
            return True
        else:
            return False

    def find_all_instances(self) -> list:
        return [self]

    def __detect(self, dist: bool = False, only_security: bool = False) -> (str, list):
        if self.pm_path:
            p = subprocess.run([self.pm_path, '-s', 'dist-upgrade' if dist else 'upgrade', '-V'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if p.stderr:
                self.print_error(p.stderr.decode("utf-8"))
                return self.pm_path, []
            out = p.stdout.decode('utf-8').strip().split('\n')
            res = []
            for s in out:
                s = s.split(" ")
                if len(s) < 5:
                    continue
                package = s[1]
                if s[0] == "Inst":
                    curr_ver = s[2][1:-1]
                    new_ver = s[3][1:]
                    if not only_security or "security" in s[4] or "security" in s[5]:
                        res.append(self.make_result_line(package, curr_ver, new_ver, "", self.colorize))
            return self.pm_path, res
        else:
            return None, []

    def detect_updates(self, only_security: bool = False) -> (str, list):
        return self.__detect(dist=False, only_security=only_security)

    def detect_dist_updates(self, only_security: bool = False) -> (str, list):
        return self.__detect(dist=True, only_security=only_security)


registry.add_packet_manager(AptPacketManager)
