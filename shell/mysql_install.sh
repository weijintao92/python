#!/bin/bash
#Date:2020-9-01
#Author:wjt
#Function: install mysql:8.0
#####################################################################
#install mysql
echo 'begin '
mkdir -p /my/lib /my/etc

#download mysql
# docker pull mysql:8.0

#Alicloud
##login Aliclou
sudo docker login --username=wtj18583708203 registry.cn-shanghai.aliyuncs.com
Wejxiaotu@1
sudo docker pull registry.cn-shanghai.aliyuncs.com/sadfasdf/docker:mysql-8.0pp

# copy mysql_data and mysql_conf
docker run -itd --name mysql-8.0 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 \
    registry.cn-shanghai.aliyuncs.com/sadfasdf/docker:mysql-8.0pp

docker cp -p mysql-8.0:/var/lib/mysql /my/lib/mysql
docker cp mysql-8.0:/etc/mysql/ /my/etc/mysql
docker stop mysql-8.0
docker rm mysql-8.0

# run mysql
# docker run -itd --name mysql-8.0 -p 3307:3306 \
#    -v /my/lib/mysql:/var/lib/mysql \
#    -v /my/etc/mysql:/etc/mysql/ \
#    -e MYSQL_ROOT_PASSWORD=123456 \
#     mysql:8.0 \

docker run -itd --name mysql-8.0 -p 3307:3306 \
   -v /my/lib/mysql:/var/lib/mysql \
   -v /my/etc/mysql:/etc/mysql/ \
   -e MYSQL_ROOT_PASSWORD=123456 \
    registry.cn-shanghai.aliyuncs.com/sadfasdf/docker:mysql-8.0pp

docker commit -a "wjt" -m "mysql_native_password" a36ffa1b5c31 my_mysql-8.0:v1
sudo docker tag 373c26b1eadd registry.cn-shanghai.aliyuncs.com/sadfasdf/docker:mysql-8.0pp
sudo docker push registry.cn-shanghai.aliyuncs.com/sadfasdf/docker:mysql-8.0pp
sudo docker pull registry.cn-shanghai.aliyuncs.com/sadfasdf/docker:mysql-8.0pp

#set mysql8.0 password  mysql_native_password
# docker exec -it mysql-8.0 /bin/bash
# mysql -u root -p
# 123456
# ALTER USER 'root'@'%' IDENTIFIED BY '123456' PASSWORD EXPIRE NEVER;
# ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
# FLUSH PRIVILEGES;