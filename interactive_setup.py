#!/usr/bin/env python
import sys
from helpers.configs_handler import ConfigsHandler
from servers_examples import servers


def main() -> None:
    src_dir = input("[+] Enter the source path to configuration files: ")
    # Check servers_example to see example servers.
    dest_dir = input("[+] Enter the destination directory to copy to: ")
    handler = ConfigsHandler(src_dir, dest_dir, servers)
    configs = handler.get_desired_configs()
    print(configs)
    answer = input("\n[+] Here are servers. Would you like to proceed? (y/n)").lower()
    if answer == "y":
        handler.copy_configs(configs)
    else:
        sys.exit("[-] Exit the program. See ya!")
    username = input("[+] Enter your username credentials for manual setup: ")
    handler.create_connections(username)


if __name__ == "__main__":
    main()
