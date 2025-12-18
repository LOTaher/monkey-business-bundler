#!/usr/bin/env python3

"""
    mbb.py - Monkey-Business-Bundler, splatte.dev's build and release system
    Copyright (C) 2025-2026 splatte.dev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import os
import time
import subprocess
import tarfile

MBB_TEXT = (
    f"\033[38;2;255;255;255mmonkey"
    f"\033[0m-"
    f"\033[38;2;2;37;84mbusiness"
    f"\033[0m-"
    f"\033[38;2;255;255;255mbundler"
    f" >\033[0m"
)


def verbose_print(str):
    local_time = time.localtime()
    formatted_time = time.strftime("%H:%M:%S", local_time)
    print(f"{MBB_TEXT} {str} ({formatted_time})")

def main():
    parser = argparse.ArgumentParser(
        prog="monkey-business-bundler",
        description="splatte.dev build and release system",
        epilog="Check out more software releases at https://splatte.dev"
    )

    parser.add_argument("-d", "--dirname", default="./", help="directory to build")
    parser.add_argument("-g", "--git", action="store_true", help="only bundle files tracked by git")
    parser.add_argument("-v", "--verbose", action="store_true", help="add verbose logging to the bundle process")

    args = parser.parse_args()

    if args.dirname == "./":
        path = os.getcwd()
    else:
        path = os.path.abspath(args.dirname)

    bundle_title = f"{os.path.basename(os.getcwd())}"

    ignore_path = f"{path}/.mbbignore"
    ignore_files = set()

    try:
        with open(ignore_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                ignore_files.add(os.path.join(path, line))
    except:
        if args.verbose:
            verbose_print("no .mbbignore file found")

    dir_files = []

    if not os.path.exists(f"{path}/.git") and args.git:
        if args.verbose:
            verbose_print("git is not initialized within this directory. bundling all files")

    if os.path.exists(f"{path}/.git") and args.git:
        if args.verbose:
            verbose_print(".git folder found. only bundling tracked files")
        tracked_files = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
        dir_files = tracked_files.stdout.split("\n")
        dir_files.pop()

        # brittle version of checking for .mbbignore when tracked by git anyways, not needed by me
        dir_files = [os.path.join(path, f) for f in dir_files if os.path.join(path, f) not in ignore_files]

        bundle_title = f"{bundle_title}-{subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()}"
    else:
        for root, dirs, files in os.walk(path):
            # mutating the dirs list directly ([:]) to prevent os.walk from going within ignored directories
            dirs[:] = [d for d in dirs if os.path.join(path, d) not in ignore_files]

            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in ignore_files:
                    dir_files.append(file_path)

    print("MBB IGNORE", ignore_files)
    print("FILES", dir_files)
    print(bundle_title)

    with tarfile.open(f"{bundle_title}.tar.gz", "w:gz") as tar:
        for file in dir_files:
            tar.add(file, arcname=os.path.relpath(file, path))

    return

if __name__ == '__main__':
    main()

