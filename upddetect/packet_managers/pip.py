# -*- coding: utf-8 -*-
from .general import PacketManager
from upddetect.common import registry
import subprocess
import re
import json
import os
import tqdm


class PipPacketManager(PacketManager):

    def __repr__(self) -> str:
        return self.pm_path if self.pm_path else "pip"

    @staticmethod
    def get_human_name() -> str:
        return "pip (package installer for Python, including pip in virtual environments)"

    @staticmethod
    def get_type() -> str:
        return "pip"

    @staticmethod
    def __find_recommended_version(affected_version: str) -> str:
        if "<=" in affected_version:
            i = affected_version.find("<=")
            return ">" + affected_version[i+2:]
        elif "<" in affected_version:
            i = affected_version.find("<")
            return ">=" + affected_version[i+1:]
        elif ">=" in affected_version:
            i = affected_version.find(">=")
            return "<" + affected_version[i+2:]
        elif ">" in affected_version:
            i = affected_version.find(">")
            return "<=" + affected_version[i+1:]
        else:
            return affected_version

    @staticmethod
    def __compare_versions(ver1: str, ver2: str) -> bool:
        """
        Returns True if ver1 > ver2, else False
        :param ver1:
        :param ver2:
        :return:
        """
        def parse_int(s: str) -> int:
            r = '0'
            for x in s:
                if x.isdigit():
                    r += x
            return int(r)
        if parse_int(ver1) > parse_int(ver2):
            return True
        else:
            return False

    def find_all_instances(self) -> list:
        venvs = []

        p = subprocess.run(["/bin/bash", "-c", "compgen -c pip"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.stderr:
            self.print_error(p.stderr.decode("utf-8"))
            return [self]
        pips = sorted(set(p.stdout.decode("utf-8").strip().split('\n')))
        pips = [
            PipPacketManager(self.which(pip), self.colorize) for pip in pips
            if pip[0:3] == "pip" and (len(pip) == 3 or pip[3].isdigit())
        ]

        paths = ["/usr/share", "/usr/local", "/home", "/opt", "/etc",
                 "/var/lib", "/var/spool", "/var/local", "/var/www"]
        progress = tqdm.tqdm(paths, ascii=True, disable=not self.colorize)
        for path in progress:
            progress.set_description(path)
            p = subprocess.run(["/usr/bin/find", path, "-name", "pyenv.cfg"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            cfgs = sorted(set(p.stdout.decode("utf-8").strip().split('\n')))
            venvs += [
                PipPacketManager(os.path.join(os.path.dirname(cfg), "/bin/pip"), self.colorize) for cfg in cfgs if cfg
            ]
        progress.set_description("done")

        return pips + venvs

    def is_available(self) -> bool:
        if PacketManager.is_available(self):
            return True

        self.pm_path = self.which("pip3")
        if not self.pm_path:
            self.pm_path = self.which("pip")

        if self.pm_path:
            return True
        else:
            return False

    def detect_updates(self, only_security: bool = False) -> (str, list):
        if self.pm_path:
            res = []
            if only_security:
                safety_path = self.which("safety")
                if not safety_path:
                    self.print_error("safety python package not found, please install it to enable the ability "
                                     "to detect security updates:\npip3 install safety")
                    return self.pm_path, []

                p1 = subprocess.run([self.pm_path, "freeze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if p1.stderr:
                    self.print_error(p1.stderr.decode("utf-8"))
                    return self.pm_path, []
                p2 = subprocess.run([safety_path, "check", "--stdin", "--json"], input=p1.stdout,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if p2.stderr:
                    if "unpinned requirement" not in p2.stderr.decode("utf-8"):
                        self.print_error(p2.stderr.decode("utf-8"))
                        return self.pm_path, []
                out = json.loads(p2.stdout.decode("utf-8").strip())
                new_out = {}
                if "vulnerabilities" not in out:
                    new_out['vulnerabilities'] = []
                    for s in out:
                        new_out['vulnerabilities'].append({
                            'package_name': s[0],
                            'vulnerable_spec': s[1],
                            'analyzed_version': s[2],
                            'advisory': s[3]
                        })
                    out = new_out

                merged = {}
                for s in out['vulnerabilities']:
                    package = s['package_name']
                    rec_ver = self.__find_recommended_version(s['vulnerable_spec'])
                    curr_ver = s['analyzed_version']
                    desc = s['advisory']
                    if package in merged:
                        merged[package]['desc'] += "\n" + desc
                        if self.__compare_versions(rec_ver, merged[package]['rec_ver']):
                            merged[package]['rec_ver'] = rec_ver
                    else:
                        merged[package] = {
                            'curr_ver': curr_ver,
                            'rec_ver': rec_ver,
                            'desc': desc
                        }
                for package in merged.keys():
                    res.append(self.make_result_line(package,
                                                     merged[package]['curr_ver'],
                                                     merged[package]['rec_ver'],
                                                     merged[package]['desc'],
                                                     self.colorize))
            else:
                p = subprocess.run([self.pm_path, "list", "--outdated"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if p.stderr:
                    stderr = p.stderr.decode("utf-8")
                    if "new release" in stderr:
                        pass
                    elif "WARNING: You are using pip version" in stderr:
                        s = stderr[stderr.find("WARNING: You are using pip version"):].split(" ")
                        res.append(self.make_result_line(s[4], s[6][0:-1], s[9], stderr, self.colorize))
                    else:
                        self.print_error(stderr)
                        return self.pm_path, []
                out = p.stdout.decode("utf-8").strip().split("\n")

                for s in out:
                    s = re.sub(" +", " ", s)
                    s = s.split(" ")
                    if s[0] == "Package" or "---" in s[0]:
                        continue
                    res.append(self.make_result_line(s[0], s[1], s[2], "", self.colorize))
            return self.pm_path, res
        else:
            return None, []


registry.add_packet_manager(PipPacketManager)
