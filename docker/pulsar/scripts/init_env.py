#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

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