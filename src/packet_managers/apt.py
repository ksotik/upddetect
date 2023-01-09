# -*- coding: utf-8 -*-
from .general import PacketManager
from src.common import registry
import subprocess


class AptPacketManager(PacketManager):

    apt_path = ""
    apt_cmd = ""

    def __repr__(self) -> str:
        return "APT"

    def is_available(self) -> bool:
        def which(s: str) -> str:
            p = subprocess.run(['which', s], stdout=subprocess.PIPE)
            return p.stdout.decode('utf-8')

        self.apt_path = which('apt-get')
        if self.apt_path:
            self.apt_cmd = "apt-get"
        if not self.apt_path:
            self.apt_path = which('apt')
            self.apt_cmd = "apt"

        if self.apt_path:
            return True
        else:
            return False

    def __detect(self, dist: bool = False, only_security: bool = False) -> list:
        if self.apt_path:
            p1 = subprocess.Popen([self.apt_cmd, '-s', 'dist-upgrade' if dist else 'upgrade', '-V'],
                                  stdout=subprocess.PIPE)
            if only_security:
                p2 = subprocess.run(['awk', '/^Inst.*security/ {print $2}'], stdin=p1.stdout, stdout=subprocess.PIPE)
            else:
                p2 = subprocess.run(['awk', '/^Inst/ {print $2}'], stdin=p1.stdout, stdout=subprocess.PIPE)
            return p2.stdout.decode('utf-8').strip().split('\n')
        return []

    def detect_updates(self, only_security: bool = False) -> list:
        return self.__detect(dist=False, only_security=only_security)

    def detect_dist_updates(self, only_security: bool = False) -> list:
        return self.__detect(dist=True, only_security=only_security)


registry.add_packet_manager(AptPacketManager)
