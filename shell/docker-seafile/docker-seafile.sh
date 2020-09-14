#!/bin/bash
#Date:2020-9-11
#Author:wjt
#Function: install docker seafile
#####################################################################

mkdir -p /my/seafile/mysql /my/seafile/shared

sudo yum -y install epel-release
yum install docker-compose -y
docker-compose up -d