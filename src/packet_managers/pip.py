# -*- coding: utf-8 -*-
from .general import PacketManager
from src.common import registry
import subprocess
import sys
import re


class PipPacketManager(PacketManager):

    def __repr__(self) -> str:
        return "pip"

    @staticmethod
    def __which(s: str) -> str:
        p = subprocess.run(['which', s], stdout=subprocess.PIPE)
        return p.stdout.decode('utf-8').strip()

    def find_all_instances(self) -> list:
        p = subprocess.run(['/bin/bash', '-c', 'compgen -c pip'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.stderr:
            # TODO: обработка ошибки
            return [self]
        pips = sorted(set(p.stdout.decode('utf-8').strip().split('\n')))
        return [PipPacketManager(self.__which(pip)) for pip in pips]

    def is_available(self) -> bool:
        if PacketManager.is_available(self):
            return True

        self.pm_path = self.__which('pip3')
        if not self.pm_path:
            self.pm_path = self.__which('pip')

        if self.pm_path:
            return True
        else:
            return False

    def detect_updates(self, only_security: bool = False) -> (str, list):

        if self.pm_path:
            if only_security:
                safety_path = self.__which('safety')
                if not safety_path:
                    print("safety python package not found, please install it to enable the ability to detect security "
                          "updates:\n\npip3 install safety",
                          file=sys.stderr)
                    return self.pm_path, []

            p = subprocess.run([self.pm_path, 'list', '--outdated'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if p.stderr:
                # TODO обработка ошибки, но работу не прерываем, если это про новую версию самого pip
                print(p.stderr)
                if not 'new release' in p.stderr.decode('utf-8'):
                    return self.pm_path, []
            out = p.stdout.decode('utf-8').strip().split('\n')
            res = []
            for s in out:
                s = re.sub(" +", " ", s)
                s = s.split(" ")
                if s[0] == "Package" or "---" in s[0]:
                    continue
                res.append(self.make_result_line(s[0], s[1], s[2]))
            return self.pm_path, res
        else:
            return None, []


registry.add_packet_manager(PipPacketManager)
