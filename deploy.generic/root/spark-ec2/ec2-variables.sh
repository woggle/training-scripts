#!/bin/bash

# These variables are automatically filled in by the mesos-ec2 script.
export MESOS_MASTERS="{{master_list}}"
export MASTERS="{{master_list}}"
export MESOS_SLAVES="{{slave_list}}"
export SLAVES="{{slave_list}}"
export ADD_SLAVES="{{add_slave_list}}"
export MESOS_ZOO_LIST="{{zoo_list}}"
export ZOO_LIST="{{zoo_list}}"
export MESOS_HDFS_DATA_DIRS="{{hdfs_data_dirs}}"
export HDFS_DATA_DIRS="{{hdfs_data_dirs}}"
export MESOS_MAPRED_LOCAL_DIRS="{{mapred_local_dirs}}"
export MAPRED_LOCAL_DIRS="{{mapred_local_dirs}}"
export MESOS_SPARK_LOCAL_DIRS="{{spark_local_dirs}}"
export SPARK_LOCAL_DIRS="{{spark_local_dirs}}"
export MODULES="{{modules}}"
export SWAP_MB="{{swap}}"

export SPARK_VERSION="{{spark_version}}"
export SHARK_VERSION="{{spark_version}}"
export HADOOP_MAJOR_VERSION=1
