#!/bin/bash
#Date:2020-9-4
#Author:wjt
#Function: install yum-config-manager
#####################################################################
echo "########################check yum-config-manager##########################"
echo "---------------------------------check yum-utils---------------------------------"
check_results=`rpm -qa | grep yum-utils`
echo $check_results
if 	[ -z $check_results ]
    then
        sudo yum install -y yum-utils
    fi
echo "---------------------------------check device-mapper-persistent-data---------------------------------"
check_results=`rpm -qa | grep device-mapper-persistent-data`
echo $check_results
if 	[ -z $check_results ]
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