#!/usr/bin/env python3
import os
from subprocess import Popen, PIPE


def get_configs(path: str) -> list:
    return os.listdir(path)


def get_ips(configs: list, path: str) -> list:
    ip_list = []
    for c in configs:
        f = os.path.join(path, c)
        with open(f, "r") as file:
            line = file.readlines()[3].strip().split(" ")[1:2]
            ip = "".join(line)
            ip_list.append(ip)
    return ip_list


def configure_ufw(ips: list) -> None:
    for ip in ips:
        cmd = Popen(f"sudo -S ufw allow out to {ip} port 1194 proto udp",
                    stdin=PIPE, stdout=PIPE,
                    stderr=PIPE, shell=True).communicate(input=b"password")
        output_list = list(cmd)
        for b in output_list:
            print(b.decode("utf-8"))


def main() -> None:
    path = input("[+] Enter path to configuration files: ")
    configs = get_configs(path)
    ip_list = get_ips(configs, path)
    configure_ufw(ip_list)


if __name__ == "__main__":
    main
