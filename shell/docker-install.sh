#!/bin/bash
#Date:2020-8-28
#Author:wjt
#Function: install docker
#####################################################################


#Step 1 check yum-config-manager
echo "########################Step 1 check yum-config-manager##########################"
echo "---------------------------------check yum-utils---------------------------------"
check_results=`rpm -qa | grep yum-utils`
echo $check_results
if 	[ -z "$check_results" ]
    then
        sudo yum install -y yum-utils
    fi
echo "---------------------------------check device-mapper-persistent-data---------------------------------"
check_results=`rpm -qa | grep device-mapper-persistent-data`
echo $check_results
if 	[ -z "$check_results" ]
    then
        sudo yum install -y device-mapper-persistent-data
    fi
echo "---------------------------------check lvm2---------------------------------"
check_results=`rpm -qa | grep lvm2-libs`
echo $check_results
if 	[ -z "$check_results" ]
    then
        sudo yum install -y lvm2
    fi
echo "########################yum-config-manager is install##########################"


#Step 2 set docker accelerate
echo "########################Step 2 set docker accelerate##########################"
sudo yum-config-manager \
    --add-repo \
    http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
#Step 3 install docker 
echo "########################Step 3 install docker ##########################"

check_results=`rpm -qa | grep docker-ce`
if 	[ -z "$check_results" ]
    then
        echo "-----------------------start install docker-ce------------------------------------"
        sudo yum install -y docker-ce
    else
        echo "-----------------------docker is already install------------------------------------"
    fi

sudo systemctl start docker
#Step 3 set  docker Image acceleration Alicloud
rm -f /etc/docker/daemon.json
echo "{\"registry-mirrors\":[\"https://9ruhy7zw.mirror.aliyuncs.com\"]}" > /etc/docker/daemon.json 
sudo systemctl daemon-reload
sudo systemctl restart docker

echo "########################docker is already success##########################"





