# test instance network performance

import commands
import json
import os
import paramiko
import random, string

#tcp_server_ip = '172.16.200.185'
#udp_server_ip = '172.16.200.184'
server_ip = '172.16.200.184'
rally_host = '25.0.0.125'

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

def test_net_tcp(file_path):
    iperf_installed = check_iperf_install()
    if iperf_installed:
        #print 'test tcp'
        (stat, out) = commands.getstatusoutput('iperf3 -c %s -t 60' % server_ip)
        if stat != 0:
            #print 'Something Error!\n %s' % out
            pass
        else:
            # write result to file first
            write_to_file(file_path, out + '\n\n')
            # the last line was what we want
            # split and get the data
            #print 'finish test tcp'
            data = out.split('\n')[-4]
            transfer_v = float(data.split()[4])
            bandwidth_v = float(data.split()[6])
            results = {}
            transfer_k = 'TCP_Transfer(' + data.split()[5] + ')'
            bandwidth_k = 'TCP_Bandwidth(' + data.split()[7] + ')'
            results[transfer_k] = transfer_v
            results[bandwidth_k] = bandwidth_v
            #print type(json.dumps(results))
            #print json.dumps(results)
            return results

def test_net_udp(file_path):
    iperf_installed = check_iperf_install()
    if iperf_installed:
        #print 'test udp'
        (stat, out) = commands.getstatusoutput('iperf3 -u -c %s -b 10000M -t 60' % server_ip)
        if stat != 0:
            #print 'Something Error!\n %s' % out
            pass
        else:
            # write result to file first
            write_to_file(file_path, out + '\n\n')
            try:
                #print 'finish test udp'
                data = out.split('\n')[-4]
                transfer_v = float(data.split()[4])
                bandwidth_v = float(data.split()[6])
                jitter_v = float(data.split()[8])
                lost_v = int(data.split()[10].split('/')[0])
                total_v = int(data.split()[-2].split('/')[-1])
                datagrams_v = float(lost_v) / float(total_v) * 100
            except Exception:
                data = out.split('\n')[-3]
            finally:
                transfer_v = float(data.split()[4])
                bandwidth_v = float(data.split()[6])
                jitter_v = float(data.split()[8])
                lost_v = int(data.split()[10].split('/')[0])
                total_v = int(data.split()[-2].split('/')[-1])
                datagrams_v = float(lost_v) / float(total_v) * 100
                results = {}
                transfer_k = 'UDP_Transfer(' + data.split()[5] + ')'
                bandwidth_k = 'UDP_Bandwidth(' + data.split()[7] + ')'
                jitter_k = 'UDP_Jitter(' + data.split()[9] + ')'
                lost_k = 'UDP_Lost'
                total_k = 'UDP_Total'
                datagrams_k = 'UDP_Datagrams(%)'
                results[transfer_k] = transfer_v
                results[bandwidth_k] = bandwidth_v
                results[jitter_k] = jitter_v
                results[lost_k] = lost_v
                results[total_k] = total_v
                results[datagrams_k] = datagrams_v
            #print type(json.dumps(results))
            #print json.dumps(results)
            return results


def exec_iperf_test():
    file_path = '/tmp/iperf_' + random_str()
    os.mknod(file_path)
    tcp_results = test_net_tcp(file_path)
    udp_results = test_net_udp(file_path)
    results = udp_results
    for k in tcp_results.keys():
        results[k] = tcp_results[k]
    #results = dict(tcp_results.items() + udp_results.items())
    # sorted the results
    #results = dict(sorted(results.iteritems(), key=lambda d:d[0]))
    #print type(results)
    # scp to rally before print
    scp_to_rally(file_path)
    print json.dumps(results)


class SSHConnection(object):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, host, username, password, port=22):
        """Initialize and setup connection"""
        self.sftp = None
        self.sftp_open = False
 
        # open SSH Transport stream
        self.transport = paramiko.Transport((host, port))
 
        self.transport.connect(username=username, password=password)
 
    #----------------------------------------------------------------------
    def _openSFTPConnection(self):
        """
        Opens an SFTP connection if not already open
        """
        if not self.sftp_open:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.sftp_open = True
 
    #----------------------------------------------------------------------
    def get(self, remote_path, local_path=None):
        """
        Copies a file from the remote host to the local host.
        """
        self._openSFTPConnection()        
        self.sftp.get(remote_path, local_path)        
 
    #----------------------------------------------------------------------
    def put(self, local_path, remote_path=None):
        """
        Copies a file from the local host to the remote host
        """
        self._openSFTPConnection()
        self.sftp.put(local_path, remote_path)
 
    #----------------------------------------------------------------------
    def close(self):
        """
        Close SFTP connection and ssh connection
        """
        if self.sftp_open:
            self.sftp.close()
            self.sftp_open = False
        self.transport.close()

def random_str(randomlength=8):
    """random file name"""
    letters = list(string.ascii_letters)
    random.shuffle(letters)
    return ''.join(letters[:randomlength])

def write_to_file(file_path, output):
    try:
        with open(file_path, 'a') as f:
            f.writelines(output)
    except Exception:
        print 'write to file error'
 
def scp_to_rally(file_path):
    username = "root"
    pw = "abc123"

    ssh = SSHConnection(rally_host, username, pw)
    # the source path was the same as destination path
    ssh.put(file_path, file_path)
    ssh.close()
    


exec_iperf_test()
