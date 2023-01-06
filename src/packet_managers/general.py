# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class PacketManager(ABC):

    @abstractmethod
    def __repr__(self) -> str:
        return "Abstract Packet Manager"
