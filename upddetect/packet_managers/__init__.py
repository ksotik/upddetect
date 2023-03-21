# -*- coding: utf-8 -*-
import importlib
import glob
from os.path import dirname, basename, isfile


modules = glob.glob(dirname(__file__) + "/*.py")
__all__ = [basename(f)[:-3] for f in modules if isfile(f)]

for module in __all__:
    if "__init__" in module or "general" in module:
        continue
    importlib.import_module("upddetect.packet_managers." + module)  # import module for adding it to the registry
