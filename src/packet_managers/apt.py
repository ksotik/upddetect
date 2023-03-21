# -*- coding: utf-8 -*-
from .general import PacketManager
from src.common import registry
import subprocess


class AptPacketManager(PacketManager):

    def __repr__(self) -> str:
        return "APT"

    def is_available(self) -> bool:
        if PacketManager.is_available(self):
            return True

        def which(s: str) -> str:
            p = subprocess.run(['which', s], stdout=subprocess.PIPE)
            return p.stdout.decode('utf-8').strip()

        self.pm_path = which('apt-get')
        if not self.pm_path:
            self.pm_path = which('apt')

        if self.pm_path:
            return True
        else:
            return False

    def find_all_instances(self) -> list:
        return [self]

    def __detect(self, dist: bool = False, only_security: bool = False) -> (str, list):
        if self.pm_path:
            p1 = subprocess.run([self.pm_path, '-s', 'dist-upgrade' if dist else 'upgrade', '-V'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if p1.stderr:
                # TODO: обработка ошибки
                return self.pm_path, []
            if only_security:
                p2 = subprocess.run(['awk', '/^Inst.*security/ {print $2}'], input=p1.stdout, stdout=subprocess.PIPE)
            else:
                p2 = subprocess.run(['awk', '/^Inst/ {print $2}'], input=p1.stdout, stdout=subprocess.PIPE)
            return self.pm_path, p2.stdout.decode('utf-8').strip().split('\n')
        else:
            return None, []

    def detect_updates(self, only_security: bool = False) -> (str, list):
        return self.__detect(dist=False, only_security=only_security)

    def detect_dist_updates(self, only_security: bool = False) -> (str, list):
        return self.__detect(dist=True, only_security=only_security)


registry.add_packet_manager(AptPacketManager)
