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

##
## Edit a properties config file and replace values based on
## the ENV variables
## export my-key=new-value
## ./apply-config-from-env file.conf
##

import argparse
import os

parser = argparse.ArgumentParser(description='apply config from env')
parser.add_argument("--env_file", type=str, required=False, help="the env file")
parser.add_argument("conf_files", nargs="+", help="the conf files")
args = parser.parse_args()

# Always apply env config to env scripts as well
conf_files = args.conf_files

PF_ENV_PREFIX = 'PULSAR_PREFIX_'
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
                os.environ[k.strip()] = v.strip()
            except:
                if PF_ENV_DEBUG:
                    print("[%s] skip env Processing %s" % (args.env_file, line))

for conf_filename in conf_files:
    lines = []  # List of config file lines
    keys = {}  # Map a key to its line number in the file

    # Load conf file
    with open(conf_filename, "r") as f:
        for line in f:
            lines.append(line)
            line = line.strip()
            if not line:
                continue

            try:
                k, v = line.split('=', 1)
                if k.startswith('#'):
                    k = k[1:]
                keys[k.strip()] = len(lines) - 1
            except:
                if PF_ENV_DEBUG:
                    print("[%s] skip Processing %s" % (conf_filename, line))

    # Update values from Env
    for k in sorted(os.environ.keys()):
        v = os.environ[k].strip()

        if v.startswith("${") and v.endswith("}"):
            v = os.environ.get(v[2:-1], "")

        # Hide the value in logs if is password.
        if "password" in k:
            displayValue = "********"
        else:
            displayValue = v

        if k.startswith(PF_ENV_PREFIX):
            k = k[len(PF_ENV_PREFIX):]
        if k in keys:
            print('[%s] Applying config %s = %s' % (conf_filename, k, displayValue))
            idx = keys[k]
            lines[idx] = '%s=%s\n' % (k, v)

    # Add new keys from Env
    for k in sorted(os.environ.keys()):
        v = os.environ[k]
        if not k.startswith(PF_ENV_PREFIX):
            continue

        if v.startswith("${") and v.endswith("}"):
            v = os.environ.get(v[2:-1], "")

        # Hide the value in logs if is password.
        if "password" in k:
            displayValue = "********"
        else:
            displayValue = v

        k = k[len(PF_ENV_PREFIX):]
        if k not in keys:
            print('[%s] Adding config %s = %s' % (conf_filename, k, displayValue))
            lines.append('%s=%s\n' % (k, v))
        else:
            print('[%s] Updating config %s = %s' % (conf_filename, k, displayValue))
            lines[keys[k]] = '%s=%s\n' % (k, v)

    # Store back the updated config in the same file
    with open(conf_filename, 'w') as f:
        for line in lines:
            f.write(line)
