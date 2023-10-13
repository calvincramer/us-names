#!/usr/bin/env python3

import subprocess
import os
from os.path import abspath, dirname, join


def sh(cmd: str, retval_expected: int = 0) -> None:
    proc = subprocess.Popen(
        args=cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        executable="/bin/bash",
    )
    stdout, stderr = proc.communicate()
    retval = proc.returncode
    stdout = "" if stdout is None else stdout.decode("utf-8", errors="replace").strip()
    stderr = "" if stderr is None else stderr.decode("utf-8", errors="replace").strip()
    if stdout != "":
        print(stdout)
    if stderr != "":
        print(stderr)
        raise Exception("Got output on stderr, exiting")
    if retval != retval_expected:
        raise Exception(f"Retval: {retval} is not 0")
    return None


def parseFile(f: str) -> dict[str, set[str]]:
    if not os.path.isfile(f):
        raise Exception(f)
    with open(f, "r") as fp:
        content = fp.readlines()
    data = {}
    for line in content:
        s = line.strip()
        if s == "":
            continue
        parts = s.split(",")
        if len(parts) != 3:
            raise Exception("Format error")
        firstName, gender, freq = parts
        if firstName in data.keys():
            data[firstName].add(gender.upper())
        else:
            data[firstName] = {gender.upper()}
    return data


def parseData() -> dict[str, set[str]]:
    data: dict[str, set[str]] = {}
    files = list(sorted(os.listdir("temp")))
    for i, f in enumerate(files):
        print(f"{f} {int(i * 100.0/len(files))}%")
        new_data = parseFile(f=join("temp", f))
        for k, v in new_data.items():
            if k in data.keys():
                data[k] = data[k].union(v)
            else:
                data[k] = v
    return data


def main():
    os.chdir(dirname(abspath(__file__)))
    if os.path.isdir("temp"):
        sh("rm -r temp")
    sh("mkdir temp")
    sh("unzip -d temp names.zip")
    data = parseData()

    # multi_gender_names = [n for n, genders in data.items() if len(genders) > 1]
    male_names = [n for n, genders in data.items() if "M" in genders]
    male_names = list(sorted(list(set(male_names))))
    print(male_names)
    with open("male_names.txt", "w+") as fp:
        for n in male_names:
            fp.write(n)
            fp.write("\n")


if __name__ == "__main__":
    main()
