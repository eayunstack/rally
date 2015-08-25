#!usr/bin/env python
# coding=utf-8
import commands
import time
import re
import socket
import fcntl
import struct

server_ip='192.168.1.122'
def test1():
    result=commands.getstatusoutput('iperf -c %s -i 10'%server_ip)
    ip_from=get_ip_address('eth0')
    try:
        myfile=open('./iperf_log.txt','a+')
        if result[0]==0:
            myresult=re.findall('\d*\.\d*\s\w*/sec',result[1])
            myfile.write('\nfrom'+ip_from+'to'+server_ip+'\t'+myresult[0]+'\t'+time.strftime('%c',time.localtime(time.time())))
        else:
            myfile.write('\n'+'ERROR\t'+result[1]+time.strftime('%c',time.localtime(time.time())))  
    finally:
        myfile.close()

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', ifname[:15]))[20:24])
 
if __name__=='__main__':
    test1()
