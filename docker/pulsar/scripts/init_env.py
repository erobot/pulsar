#!/usr/bin/env python

__author__ = "qunzhong"

import argparse
import os
import sys

try:  # py3
    from shlex import quote
except ImportError:  # py2
    from pipes import quote

parser = argparse.ArgumentParser(description='init env form env.conf')
parser.add_argument("--env_file", type=str, required=True, help="the env file")
# parser.add_argument("env_file", nargs="+", help="the conf files")
args = parser.parse_args()

PF_ENV_DEBUG = (os.environ.get('PF_ENV_DEBUG', '0') == '1')

# Try load env file
if args.env_file:
    with open(args.env_file, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue

            try:
                k, v = line.split('=', 1)
                command = 'export %s=%s' % (str(k), str(v))
                # print(command)
                # os.system(command)
                print('export {}={}'.format(str(k),quote(str(v))))
            except:
                print("[%s] skip env Processing %s" % (args.env_file, line))