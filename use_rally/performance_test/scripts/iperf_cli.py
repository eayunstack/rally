#!usr/bin/env python
# coding=utf-8
import commands
import time
import re
import socket
import fcntl
import struct
#client端需要先安装sshpass,sshpass用以在登录服务器端时,直接在命令行中指定密码.
#初次使用,先手动ssh到server端,建立认证,就是自己输入'yes'.否则就无法取到server的hostname.
server_ip='192.168.1.122'
pwd='1q2w3e'
server_name='yeming'
def iperf_cli():
    result=commands.getstatusoutput('iperf -c %s'%server_ip)
    hostname=commands.getstatusoutput('cat /etc/hostname')
    server=commands.getstatusoutput('sshpass -p "%s" ssh %s@%s "cat /etc/hostname"'%(pwd,server_name,server_ip,))
    # print server
    try:
        myfile=open('./iperf_log.txt','a+')
        if result[0]==0:
            myresult=re.findall('\d*\.\d*\s\w*/sec',result[1])
            myresult1='\t'.join(myresult)
            myfile.write('\nfrom\t'+hostname[1]+'\tto\t'+server[1]+'\tBandwidth->'+myresult1+'\t'+time.strftime('%c',time.localtime(time.time())))
        else:
            myfile.write('\n'+'ERROR\t'+result[1]+time.strftime('%c',time.localtime(time.time())))  
    finally:
        myfile.close()

if __name__=='__main__':
    iperf_cli()
