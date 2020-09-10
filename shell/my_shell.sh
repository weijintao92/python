#!/bin/bash
#Date:2020-8-28
#Author:wjt
#Function: Build docker, nginx, mysql, Tomcat
#####################################################################
#remove doceker
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
#install yum-config-manager
sudo yum install -y yum-utils \
  device-mapper-persistent-data \
  lvm2
#set docker Repository
sudo yum-config-manager \
    --add-repo \
    https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/centos/docker-ce.repo
#install docker
sudo yum install -y docker-ce docker-ce-cli containerd.io
#start docker
sudo systemctl start docker
#set docker Image acceleration Alicloud
rm -f /etc/docker/daemon.json
echo "{"registry-mirrors":["https://9ruhy7zw.mirror.aliyuncs.com"]}" > /etc/docker/daemon.json 
sudo systemctl daemon-reload
sudo systemctl restart docker
#install mysql
mkdir -p /my/mysql /my/mysql/conf
docker pull mysql:8.0
docker run -itd --name mysql-8.0 -p 3307:3306 \
   -v /my/mysql:/var/lib/mysql \
   -v /my/mysql/conf:/etc/mysql/ \
   -e MYSQL_ROOT_PASSWORD=123456 \
    mysql:8.0
#set mysql8.0 password  mysql_native_password
docker exec -it mysql-8.0 /bin/bash
mysql -u root -p
123456
ALTER USER 'root'@'%' IDENTIFIED BY '123456' PASSWORD EXPIRE NEVER;
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
FLUSH PRIVILEGES;

