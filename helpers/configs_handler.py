import os
import random
import shutil
import re
import subprocess


class Helper():
    def __init__(self, src_dir: str, dest_dir: str, servers: tuple):
        self.src_dir = src_dir
        self.dest_dir = dest_dir
        self.servers = servers

    @staticmethod
    def _list_dir(dir: list) -> list:
        return os.listdir(dir)

    @staticmethod
    def _get_active_conn() -> list:
        cmd = subprocess.run(
            "nmcli --fields NAME,TYPE con show | grep vpn", capture_output=True, text=True, shell=True)
        vpn_connections = cmd.stdout.split()
        filtered = list(filter(lambda c: c != "vpn", vpn_connections))
        return filtered


    def _filter_nedeed(self, configs: list) -> list:
        # filter according to servers
        single_connection = [list(filter(lambda x: re.search("^" + s + "\d", x), configs)) for s in self.servers]
        double_connection = [list(filter(lambda x: re.search("^" + s + "\D[a-z]{2}\d", x), configs)) for s in self.servers]
        # get rid of empty lists
        connections = list(filter(lambda x: x, [*single_connection, *double_connection]))
        # choose four random servers for each location
        randomized = list(map(lambda x: random.choices(x, k=4), connections))
        # get rid of nested lists
        return [_ for r in randomized for _ in r]


class ConfigsHandler(Helper):
    def __init__(self, src_dir: str, dest_dir: str, servers: tuple):
        super().__init__(src_dir, dest_dir, servers)

    def get_desired_configs(self) -> list:
        configs = self._list_dir(self.src_dir)

        return self._filter_nedeed(configs)

    def copy_configs(self, configs: list) -> None:
        for config in configs:
            f = os.path.join(self.src_dir, config)
            path = shutil.copy(f, self.dest_dir)
            print(f"Path to the configuration file: {path}")

    def create_connections(self, dest: str, username: str) -> None:
        configs = self._list_dir(dest)
        for config in configs:
            f = os.path.join(dest, config)
            import_conn = subprocess.run(f"nmcli connection import type openvpn file {f}", capture_output=True, text=True,
                                         shell=True)
            if import_conn.returncode == 0:
                conn_name = config.replace(".ovpn", "")
                subprocess.run(
                    f"nmcli connection modify {conn_name} vpn.user-name {username}", shell=True)
                print(import_conn.stdout)

    def delete_connections(self) -> None:
        vpn_connections = self._get_active_conn()
        for conn in vpn_connections:
            delete_cmd = subprocess.run(
                f"nmcli connection delete {conn}", capture_output=True, text=True, shell=True)
            print(delete_cmd.stdout)
