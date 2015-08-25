#!usr/bin/env python
# coding=utf-8
import commands
import time
server_ip='192.168.1.122'
def test1():
    result=commands.getstatusoutput('iperf -c %s -t 10'%server_ip)
    try:
        myfile=open('./iperf_log.txt','a+')
        if result[0]==0:
            myfile.write(result[1]+time.strftime('%c',time.localtime(time.time())))
        else:
            myfile.write('\n'+'ERROR\t'+result[1]+time.strftime('%c',time.localtime(time.time())))  
    finally:
        myfile.close() 
if __name__=='__main__':
    test1()
