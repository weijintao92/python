#!/bin/bash
#Date:2020-9-01
#Author:wjt
#Function: docker install mysql:8.0
#####################################################################
echo '########################### Step 1 create real mac mapping catalog##################################### '
mkdir -p /my/lib /my/etc
echo '########################### Step 2 check Expect##################################### '
check_results=`rpm -qa | grep expect`
echo $check_results
if 	[ -z "$check_results" ]
    then
        sudo yum install -y expect
    fi
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
echo '########################### Step 5 begin mysql:8.0 images##################################### '
# copy mysql_data and mysql_conf
docker run -itd --name ${my_name} -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 registry.cn-shanghai.aliyuncs.com/sadfasdf/docker:${my_tag}
docker cp ${my_name}:/var/lib/mysql /my/lib/
docker cp ${my_name}:/etc/mysql/ /my/etc/
docker stop ${my_name}
docker rm ${my_name}
echo '########################### Step 6 run mysql:8.0 images##################################### '
# run mysql
docker run -itd --name ${my_name} -p 3307:3306 \
   -v /my/lib/mysql:/var/lib/mysql \
   -v /my/etc/mysql:/etc/mysql/ \
   -e MYSQL_ROOT_PASSWORD=123456 \
    registry.cn-shanghai.aliyuncs.com/sadfasdf/docker:${my_tag}


# #set mysql8.0 password  mysql_native_password
# # docker exec -it mysql-8.0 /bin/bash
# # mysql -u root -p
# # 123456
# # ALTER USER 'root'@'%' IDENTIFIED BY '123456' PASSWORD EXPIRE NEVER;
# # ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
# # FLUSH PRIVILEGES;