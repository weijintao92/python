#!/bin/bash
#Date:2020-9-01
#Author:wjt
#Function: mysql_native_password
#####################################################################
mysql -u root -p
123456
ALTER USER 'root'@'%' IDENTIFIED BY '123456' PASSWORD EXPIRE NEVER;
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';
FLUSH PRIVILEGES;