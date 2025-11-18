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
    # parser.add_argument("-v", "--version", action="store_true", default="", help="the bundle version (defaults to git hash if feasible)")
    parser.add_argument("-v", "--verbose", action="store_true", help="add verbose logging to the bundle process")

    args = parser.parse_args()

    if args.dirname == "./":
        path = os.getcwd()
    else:
        path = os.path.abspath(args.dirname)

    if args.verbose:
        verbose_print(f"Found path {path}")

    files = os.listdir(path)

    if args.verbose:
        if ".git" not in files and args.git:
            verbose_print("git is not initialized within directory, using directory's name")

    return

if __name__ == '__main__':
    main()

