# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class PacketManager(ABC):

    @abstractmethod
    def __repr__(self) -> str:
        return "Abstract Packet Manager"

    @abstractmethod
    def is_available(self) -> bool:
        return False

    @abstractmethod
    def detect_updates(self, only_security: bool = False) -> list:
        return []

    @abstractmethod
    def detect_dist_updates(self, only_security: bool = False) -> list:
        return []
