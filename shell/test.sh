#!/bin/bash

echo '########################### Step 3 login my aliyun Warehouse##################################### '
/usr/bin/expect <<EOF
    spawn sudo docker login --username=wtj18583708203 registry.cn-shanghai.aliyuncs.com
    expect "*password"
    send "Weixiaotu@1\n"
    expect eof
EOF
echo '########################### Step 4 download mysql:8.0 images##################################### '
my_tag="mysql8"
my_name="mysql-8.0"
check_results=`docker images | grep registry.cn-shanghai.aliyuncs.com/sadfasdf/docker|grep ${my_tag}`
echo $check_results
if 	[ -z "$check_results" ]
    then
        sudo docker pull registry.cn-shanghai.aliyuncs.com/sadfasdf/docker:${my_tag}
    fi