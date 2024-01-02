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


def parseFile(f: str) -> dict[str, tuple[set[str], int]]:
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
        freq = int(freq)
        if firstName in data.keys():
            curr_genders, curr_freq = data[firstName]
            data[firstName] = (curr_genders | set(gender.upper()), curr_freq + freq)
        else:
            data[firstName] = ({gender.upper()}, freq)
    return data


def parseData() -> dict[str, tuple[set[str], int]]:
    data = {}
    files = list(sorted(os.listdir("temp")))
    for i, f in enumerate(files):
        print(f"{f} {int(i * 100.0/len(files))}%")
        new_data = parseFile(f=join("temp", f))
        for k, v in new_data.items():
            new_genders, new_freq = v
            if k in data.keys():
                curr_genders, curr_freq = data[k]
                data[k] = (curr_genders.union(new_genders), curr_freq + new_freq)
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

    m = lambda x: "M" in x
    f = lambda x: "F" in x
    multi = lambda x: len(x) > 1

    for cond, filename in [
        (m, "male_names.txt"),
        (f, "female_names.txt"),
        (multi, "unisex_names.txt"),
    ]:
        names = [n for n, (genders, freq) in data.items() if cond(genders)]
        names_uniq = list(sorted(list(set(names))))
        with open(filename, "w+") as fp:
            for n in names_uniq:
                fp.write(n)
                fp.write("\n")
        names_count = {n: freq for n, (genders, freq) in data.items() if cond(genders)}
        with open(f"{filename}.count", "w+") as fp:
            for name in sorted(names_count, key=names_count.get, reverse=True):
                count = names_count[name]
                fp.write(f"{count}\t{name}\n")


if __name__ == "__main__":
    main()
