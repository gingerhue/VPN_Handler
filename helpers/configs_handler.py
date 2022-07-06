import os
import random
import shutil
import subprocess


class Helper():
    def __init__(self, src_dir: str, abbrs: list, dest_dir: str):
        self.src_dir = src_dir
        self.abbrs = abbrs
        self.dest_dir = dest_dir

    @staticmethod
    def _list_dir(dir: list) -> list:
        return os.listdir(dir)

    @staticmethod
    def _get_random_config(configs: list, abbr: str) -> str:
        configs_list = [config for config in configs if abbr in config]
        if not configs_list:
            raise IndexError("Incorrect abbreviation. Try again!")
        else:
            return random.choice(configs_list)

    @staticmethod
    def _get_active_conn() -> list:
        cmd = subprocess.run(
            "nmcli --fields NAME,TYPE con show | grep vpn", capture_output=True, text=True, shell=True)
        vpn_connections = cmd.stdout.split()
        filtered = list(filter(lambda c: c != "vpn", vpn_connections))
        return filtered


class ConfigsHandler(Helper):
    def __init__(self, src_dir: str, dest_dir: str, *abbrs: str):
        super().__init__(src_dir, abbrs, dest_dir)

    def get_desired_configs(self) -> list:
        configs = self._list_dir(self.src_dir)
        servers = [self._get_random_config(
            configs, a) for a in self.abbrs]
        return servers

    def copy_configs(self) -> None:
        configs = self.get_desired_configs()
        for config in configs:
            f = os.path.join(self.src_dir, config)
            path = shutil.copy(f, self.dest_dir)
            print(f"Path to the configuration file: {path}")

    def create_connections(self, username: str) -> None:
        configs = self._list_dir(self.dest_dir)
        for config in configs:
            f = os.path.join(self.dest_dir, config)
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
