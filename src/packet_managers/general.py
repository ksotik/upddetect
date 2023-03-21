# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
import os


class PacketManager(ABC):

    pm_path = ""

    def __init__(self, instance_path: str = ""):
        self.pm_path = instance_path

    @abstractmethod
    def __repr__(self) -> str:
        return "Abstract Packet Manager"

    def is_available(self) -> bool:
        if self.pm_path:
            if not os.path.isfile(self.pm_path):
                # TODO: обработка ошибки
                return False
            if not os.access(self.pm_path, os.X_OK):
                # TODO: обработка ошибки
                return False
            return True

    def detect_updates(self, only_security: bool = False) -> (str, list):
        return None, []

    def detect_dist_updates(self, only_security: bool = False) -> (str, list):
        return None, []

    def find_all_instances(self) -> list:
        return []

    def make_result_line(self, package: str, current_version: str, latest_version: str) -> dict:
        return {
            'package': package,
            'current': current_version,
            'latest': latest_version
        }
