# -*- coding: utf-8 -*-
from .general import PacketManager
from src.common import registry
import subprocess


class AptPacketManager(PacketManager):

    apt_path = ""

    def __repr__(self) -> str:
        return "APT"

    def is_available(self) -> bool:
        def which(s: str) -> str:
            r = subprocess.run(['which', s], stdout=subprocess.PIPE)
            return r.stdout.decode('utf-8')

        self.apt_path = which('apt-get')
        if not self.apt_path:
            self.apt_path = which('apt')
        if not self.apt_path:
            self.apt_path = which('aptitude')

        if self.apt_path:
            return True
        else:
            return False

    def detect_updates(self, only_security=False) -> list:
        if self.apt_path.find('apt-get') >= 0:
            # apt-get -s dist-upgrade -V | awk '/^Inst/ {print $2}'
            r = subprocess.run(['apt-get', '-s', 'upgrade', '-V', '|', 'awk', "'/^Inst/ {print $2}'"],
                               stdout=subprocess.PIPE)
            return r.stdout.decode('utf-8').split('\n')
        return []


registry.add_packet_manager(AptPacketManager)
