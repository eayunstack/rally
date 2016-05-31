# test instance network performance

import commands
import sys
import json

tcp_server_ip = '25.0.0.211'
udp_server_ip = '25.0.0.212'

def _network_get_nic_status():
    # need to rewrite
    tmp = glob.glob('/sys/class/net/*/device')
    nics = dict()
    for i in tmp:
        name = i.split('/')[4]
        (status, out) = commands.getstatusoutput(
            "ethtool %s | \grep 'Link detected:'" % (name))
        if 'yes' in out:
            status = 'yes'
        else:
            status = 'no'
        nics[name] = status
    return nics

def install_iperf():
    # if can ping internet...
    while True:
        #print 'check Internet'
        (ping_s, ping_out) = commands.getstatusoutput('ping -c 3 baidu.com')
        if ping_s !=0:
            #print 'Internet Unreachable!\n'
            with open('/etc/resolv.conf', 'a') as f:
                f.write('nameserver 114.114.114.114')
        else:
            #print 'check wget'
            (check_wget, o) = commands.getstatusoutput('which wget')
            if check_wget:
                #print 'install wget'
                (wget_s, wget_out) = commands.getstatusoutput('yum -y install wget')
            #print 'install iperf'
            (install_s, install_out) = commands.getstatusoutput('wget https://iperf.fr/download/iperf_2.0.5/iperf_2.0.5-2_amd64 ; chmod +x iperf_2.0.5-2_amd64 ; sudo mv iperf_2.0.5-2_amd64 /usr/bin/iperf')
            if install_s != 0:
                #print 'Install Failed: \n%s' % install_out
                # install failed
                return 1
            else:
                # install successfully
                #print 'Install Successfully'
                return 0

def check_iperf_install():
    # if install
    (check_s, check_out) = commands.getstatusoutput('which iperf')
    installed = check_s
    if check_s:
        i = 0
        while True:
            if i == 10:
                #print 'I have tried %s times, failed. never tried again!\n' % i
                return 0
            elif installed != 0:
                installed = install_iperf()
                i += 1
            else:
                break
    return 1

def test_net_tcp():
    iperf_installed = check_iperf_install()
    if iperf_installed:
        #print 'test tcp'
        (stat, out) = commands.getstatusoutput('iperf -c %s -t 120' % tcp_server_ip)
        if stat != 0:
            #print 'Something Error!\n %s' % out
            pass
        else:
            # the last line was what we want
            # split and get the data
            #print 'finish test tcp'
            data = out.split('\n')[-1]
            transfer = float(data.split()[4])
            bandwidth = float(data.split()[6])
            results = {}
            results['TCP_Transfer'] = transfer
            results['TCP_Bandwidth'] = bandwidth
            #print type(json.dumps(results))
            print json.dumps(results)
            return results

def test_net_udp():
    iperf_installed = check_iperf_install()
    if iperf_installed:
        #print 'test udp'
        (stat, out) = commands.getstatusoutput('iperf -u -c %s -f M -b 1000M -t 120' % udp_server_ip)
        if stat != 0:
            #print 'Something Error!\n %s' % out
            pass
        else:
            #print 'finish test udp'
            data = out.split('\n')[-1]
            transfer = float(data.split()[4])
            bandwidth = float(data.split()[6])
            jitter = float(data.split()[8])
            lost = int(data.split()[10].split('/')[0])
            total = int(data.split()[-2].split('/')[-1])
            datagrams = float(lost) / float(total)
            results = {}
            results['UDP_Transfer'] = transfer
            results['UDP_Bandwidth'] = bandwidth
            results['UDP_Jitter'] = jitter
            results['UDP_Lost'] = lost
            results['UDP_Total'] = total
            results['UDP_Datagrams'] = datagrams
            #print type(json.dumps(results))
            print json.dumps(results)
            return results


#test_net_tcp()
test_net_udp()
#sys.exit(0)
