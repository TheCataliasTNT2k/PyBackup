#!/usr/bin/python3.8

import json
import os
from argparse import ArgumentParser
from datetime import date, time, datetime, timedelta
from sys import exit
import hashlib

from config_check import Config, create_from_json


def get_backup_path(config: Config):
    path = config.backup_dir
    if not path.endswith("/"):
        path += "/"

    # get the current date
    current_date = date.today()

    # check if the script has been executed before the backup job has
    # been started / before it can be completed (defined as START_CHECK)
    if datetime.now().time() < time(hour=config.time_hour, minute=config.time_minute):
        # check the backup of yesterday
        current_date -= timedelta(1)

    path += str(current_date)
    return path


def main(config_path: str):
    config: Config = create_from_json(json.load(open(config_path, "r")))
    config.verify_settings()

    backup_location = get_backup_path(config)

    if os.path.isdir(backup_location):
        files = [file for file in os.listdir(backup_location) if os.path.isfile(os.path.join(backup_location, file))]

        for database in config.database_list:
            if f"{database}.sql" not in files:
                print(f"Missing backup of database \"{database}\"")
                exit(1)

        for path in config.file_path_list:
            if path.endswith("/"):
                path = path[:-1]
            path = os.path.basename(path)
            if f"{os.path.basename(path)}.tar.gz" not in files:
                print(f"Missing backup of file or folder \"{path}\"")
                exit(1)

        # check check sums
        methods: list = ["sha512", "sha384", "sha256", "sha224", "sha1", "md5"]

        for method in methods:
            if f"{method}sum.txt" not in files:
                print(f"Warning: Missing checksum file \"{method}sum.txt\"!")
                continue
            with open(f"{backup_location}/{method}sum.txt", "r") as check_sum_file:
                for entry in check_sum_file.readlines():
                    checksum, filename = entry.replace("\n", "").split("\t")
                    if not os.path.isfile(f"{backup_location}/{filename}"):
                        print(f"Warning: There is a checksum for \"{os.path.basename(filename)}\""
                              f" in \"{method}sum.txt\", but the file does not exist")
                        continue
                    if checksum != getattr(hashlib, method)(
                            open(f"{backup_location}/{filename}", "rb").read()).hexdigest():
                        print(f"{method} checksum of \"{os.path.basename(filename)}\" is not correct!")
                        exit(1)

        if config.file_path_list:
            for sum in config.checksums:
                if f"{sum}sum.txt" not in files:
                    print(f"Warning: Missing \"{sum}\" check sums for the file backup!")
                    exit(1)

        print("Ok!")
        exit(0)
    else:
        print("Backup not found!")
        exit(1)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", help="config file", nargs=1)

    # get arguments
    args = vars(parser.parse_args())

    main(args.get("config")[0] if args.get("config") else ".config.json")
