#!/usr/bin/env python3

import subprocess
import os
from os.path import abspath, dirname


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


def main():
    os.chdir(dirname(abspath(__file__)))
    sh("mkdir temp")
    sh("unzip -d temp")
    # For each file parse data
    sh("ls temp")
    sh("rm -r temp")
