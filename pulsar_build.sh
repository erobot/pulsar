#!/usr/bin/env bash
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


PULSAR_DEPLOY_DIR=$1
PULSAR_SOURCE_DIR=`pwd`
PULSAR_VERSION=2.8.3


# maven build project
mvn clean install -DskipTests -T 8
if [ $? -eq 0 ]; then
    echo "maven build succeed."
else
    echo "mvn build failed. exit"
    exit 1
fi

if [ "${PULSAR_DEPLOY_DIR}x" = "x" ];
    then
    echo "if you want deploy pulsar, please set deploy dir first."
    exit 1
fi

if [ ! -d  $PULSAR_DEPLOY_DIR/pulsar ]; then
    mkdir -p $PULSAR_DEPLOY_DIR/pulsar
fi
# copy pulsar-src-code to deploy dir
tar xfz $PULSAR_SOURCE_DIR/distribution/server/target/apache-pulsar-$PULSAR_VERSION-bin.tar.gz -C $PULSAR_SOURCE_DIR/distribution/server/target
cp -ri $PULSAR_SOURCE_DIR/distribution/server/target/apache-pulsar-$PULSAR_VERSION/. $PULSAR_DEPLOY_DIR/pulsar


# generate conf tql
cp $PULSAR_DEPLOY_DIR/pulsar/conf/zookeeper.conf $PULSAR_DEPLOY_DIR/pulsar/conf/zookeeper.conf.tpl
cp $PULSAR_DEPLOY_DIR/pulsar/conf/broker.conf $PULSAR_DEPLOY_DIR/pulsar/conf/broker.conf.tpl
cp $PULSAR_DEPLOY_DIR/pulsar/conf/bookkeeper.conf $PULSAR_DEPLOY_DIR/pulsar/conf/bookkeeper.conf.tpl

# copy deploy scripts to depoly bin dir
cp $PULSAR_SOURCE_DIR/docker/pulsar/scripts/init_env.py $PULSAR_DEPLOY_DIR/pulsar/bin
chmod 755 $PULSAR_DEPLOY_DIR/pulsar/bin/init_env.py
cp $PULSAR_SOURCE_DIR/docker/pulsar/scripts/apply-config-from-env.py $PULSAR_DEPLOY_DIR/pulsar/bin
cp $PULSAR_SOURCE_DIR/docker/pulsar/scripts/apply-config-from-env-with-prefix.py $PULSAR_DEPLOY_DIR/pulsar/bin
cp $PULSAR_SOURCE_DIR/docker/pulsar/scripts/gen-yml-from-env.py $PULSAR_DEPLOY_DIR/pulsar/bin
cp $PULSAR_SOURCE_DIR/docker/pulsar/scripts/generate-zookeeper-config.sh $PULSAR_DEPLOY_DIR/pulsar/bin
cp $PULSAR_SOURCE_DIR/docker/pulsar/scripts/pulsar-zookeeper-ruok.sh $PULSAR_DEPLOY_DIR/pulsar/bin
cp $PULSAR_SOURCE_DIR/docker/pulsar/scripts/watch-znode.py $PULSAR_DEPLOY_DIR/pulsar/bin

# add offloaders
tar xfz $PULSAR_SOURCE_DIR/distribution/offloaders/target/apache-pulsar-offloaders-$PULSAR_VERSION-bin.tar.gz -C $PULSAR_SOURCE_DIR/distribution/offloaders/target
cp -ri $PULSAR_SOURCE_DIR/distribution/offloaders/target/apache-pulsar-offloaders-$PULSAR_VERSION/offloaders/. $PULSAR_DEPLOY_DIR/pulsar/offloaders

# add connectors
cp -ri $PULSAR_SOURCE_DIR/distribution/io/target/apache-pulsar-io-connectors-$PULSAR_VERSION-bin $PULSAR_DEPLOY_DIR/pulsar/connectors


#maybe useless, ignore
# cpp-client : no need at 2.8.2 : https://github.com/apache/pulsar/pull/9811
# python-client : python-client will generate after ./docker/build.sh which config in docker/pulsar/pom.xml

