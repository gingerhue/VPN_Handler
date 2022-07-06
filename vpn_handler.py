#!/usr/bin/env python3
import os
from time import sleep
import subprocess
import random
import tempfile
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt="%m/%d/%Y %I:%M:%S %p",
                    level=logging.INFO)
logger = logging.getLogger("VPNHandler")


class VPNHandler:

    @staticmethod
    def _get_connections() -> list:
        network = subprocess.run("nmcli --fields NAME,TYPE con show | grep vpn",
                                 capture_output=True, text=True, shell=True)
        vpn_connections = network.stdout.split()
        return list(filter(lambda c: c != "vpn", vpn_connections))

    @staticmethod
    def _if_connected() -> bool:
        conn_check = subprocess.run(
            'nmcli con show --active | grep vpn', capture_output=True, text=True, shell=True)
        return 'vpn' in conn_check.stdout

    @staticmethod
    def _passwd_temp_file() -> str:
        temp = tempfile.NamedTemporaryFile(mode="w+t", delete=False).name
        lookup_passwd = subprocess.run(
            "secret-tool lookup [attribute] [value]", capture_output=True, text=True, shell=True)
        with open(temp, "w") as file:
            file.write(f"vpn.secrets.password:{lookup_passwd.stdout}")
        return temp

    def open_conn(self) -> None:
        while True:
            try:
                if self._if_connected():
                    pass
                else:
                    random_server = random.choice(self._get_connections())
                    tmp_passwd = self._passwd_temp_file()
                    conn_to_vpn = subprocess.run(
                        f'nmcli con up {random_server} passwd-file {tmp_passwd}', capture_output=True, shell=True)

                    os.remove(tmp_passwd)
                    if conn_to_vpn.returncode == 0:
                        logger.info(f"Connected to {random_server}")
                    else:
                        logger.info(
                            f"Unable to connect to {random_server}. Trying again...")
                sleep(5)
            except KeyboardInterrupt:
                print('[-] Keyboard interruption. See you!')
                exit()


def main() -> None:
    VPNHandler().open_conn()


if __name__ == '__main__':
    main()
