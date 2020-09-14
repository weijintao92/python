#!/bin/bash
#Date:2020-9-11
#Author:wjt
#Function: yum init


sudo yum -y install epel-release

echo "########################Step 1 backup repo##########################"
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
echo "########################Step 1 download repo ##########################"
curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.163.com/.help/CentOS7-Base-163.repo
yum clean all

