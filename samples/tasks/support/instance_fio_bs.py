# test instance disk performance
# wiki: http://wiki.mikejung.biz/Benchmarking

import commands
import re
import json
import paramiko
import random, string
import os


<<<<<<< HEAD
iodepth = '4'
rw = 'randwrite'
iodepth = '1'


def _net_get_nic_status():
    # need to rewrite
    pass

def instal_fio():
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
            (install_s, install_out) = commands.getstatusoutput('wget http://pkgs.repoforge.org/fio/fio-2.1.10-1.el7.rf.x86_64.rpm; sudo yum -y localinstall fio-2.1.10-1.el7.rf.x86_64.rpm')
            if install_s != 0:
                #print 'Install Failed: \n%s' % install_out
                # install failed
                return 1

def check_fio():
    # check if fio was installed
    (check_s, check_o) = commands.getstatusoutput('which fio')
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

def test_fio_bs(file_path):
    fio_installed = check_fio()
    if fio_installed:
        bs_args = ['4k', '8k', '16k', '64k', '512k', '1M', '2M', '4M', '8M']
        results = {}
        (checkdisk_s, checkdisk_o) = commands.getstatusoutput('ls /dev/vdb')
        if checkdisk_s !=0:
            (s, o) = commands.getstatusoutput('fdisk -l')
            os.mknod('/tmp/disk')
            write_to_file('/tmp/disk', o)
            scp_to_rally('/tmp/disk')
            print 'no disk'
        else:
            for bs in bs_args:
                (stat, out) = commands.getstatusoutput('fio -ioengine=libaio -bs=%s -direct=1\
                                                        -thread -rw=%s -size=100G\
                                                        -filename=/dev/vdb\
                                                        -name="FIO with bs"\
                                                        -iodepth=%s -runtime=30'
                                                        % (bs, rw, iodepth))
                if stat !=0:
                    # error
                    print 'error'
                else:
                    # write to file
                    title = '\n\n====================  bs=' + bs + '  ====================\n'
                    write_to_file(file_path, title)
                    write_to_file(file_path, out)
                    #print out
                    results[bs] = out
    else:
        print 'fio not install'
    #print results
    return results

def _results():
    # excute test and output results
    file_path = '/tmp/' + 'fio_bs_' + random_str()
    os.mknod(file_path)
    results_dict = test_fio_bs(file_path)
    output_info = {}
    for key in results_dict.keys():
        results = results_dict[key].split('\n')
        # the read: line is useful
        useful_line = results[5]
        bw_v = re.findall(r'[\d|.]+', useful_line.split(', ')[1])[0]
        # add KB/s or B/s
        bw_k = key + '_bw(' + useful_line.split(', ')[1].split(bw_v)[-1] + ')'
        output_info[bw_k] = float(bw_v)
        iops_k = key + '_iops'
        iops_v = useful_line.split(', ')[2].split('=')[-1]
        output_info[iops_k] = float(iops_v)
        utils_k = key + '_utils(%)'
        utils_line = results[-1]
        utils_v = re.findall(r'[\d|.]+', utils_line.split(', ')[-1])[0]
        output_info[utils_k] = float(utils_v)
    # scp to rally before output
    scp_to_rally(file_path)
    print json.dumps(output_info)
    return output_info

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
    host = "25.0.1.254"
    username = "root"
    pw = "abc123"

    ssh = SSHConnection(host, username, pw)
    # the soure path was the same as destination path
    ssh.put(file_path, file_path)
    ssh.close()
    


_results()
