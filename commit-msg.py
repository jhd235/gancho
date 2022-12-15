#!/usr/bin/env python
import argparse
import sys
import os

COMMIT_EDITMSG = ".git/COMMIT_EDITMSG"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=str, default=COMMIT_EDITMSG,
                        help="the path of commit message file")
    args = parser.parse_args()
    msg = read_msg(args.path)
    if not msg.strip():
        print(f"ֿ\nerror:\tcommit message can't be empty\n")
        sys.exit(1)
    run_hook(msg)

def read_msg(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as file:
            msg = file.read()
            # cut the commented text
            msg = msg.split("#", 1)[0]
    except FileNotFoundError:
        print(f"\n\
error:\tthe path  {path}  not found!\n\
hint:\tthe commit message is usually stored in  {COMMIT_EDITMSG}\n")
        sys.exit(1)
    return msg

def run_hook(msg: str):
    global default_prefixes
    skip = check_skip(msg)
    skip = skip.replace("['[", '')
    skip = skip.replace("]']", '')
    if skip:
        command = skip + " pre-commit run --all-files" #command to be executed
        res = os.system(command)
        sys.exit(1)
    sys.exit(0)

def check_skip(msg: str) -> str:
    import re
    errors = ""
    res = re.findall(r'\[.*?\]', msg)
    errors += "SKIP=" + str(res)
    return errors

if __name__ == "__main__":
    exit(main())
