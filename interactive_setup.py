#!/usr/bin/env python3
from helpers.configs_handler import ConfigsHandler


def main() -> None:
    src_dir = input("[+] Enter the source path to configuration files: ")
    # Check servers_example to see example servers.
    abbrs = input("[+] Enter abbreviations of desired servers.\n"
                  "Example: uk it se-nl.\n"
                  "Use space as a delimiter: ")
    dest_dir = input("[+] Enter the destination directory to copy to: ")
    abbrs_list = abbrs.lower().split()
    handler = ConfigsHandler(src_dir, dest_dir, *abbrs_list)
    handler.copy_configs()
    username = input("[+] Enter your username credentials for manual setup: ")
    handler.create_connections(username)


if __name__ == "__main__":
    main()
