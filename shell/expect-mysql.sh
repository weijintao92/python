#!/bin/bash
#Date:2020-9-01
#Author:wjt
#Function: docker expect
#####################################################################

spawn sudo docker login --username=wtj18583708203 registry.cn-shanghai.aliyuncs.com
expect "*password"
send "Weixiaotu@1\n"
expect eof