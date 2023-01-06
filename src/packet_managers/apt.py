# -*- coding: utf-8 -*-
from .general import PacketManager
from src.common import registry
import subprocess


class AptPacketManager(PacketManager):

    def __repr__(self) -> str:
        return "APT"

    def is_available(self) -> bool:
        r = subprocess.run(['which', 'apt-get'], stdout=subprocess.PIPE)
        s = r.stdout.decode('utf-8')
        print(s)
        return True


registry.add_packet_manager(AptPacketManager)
