#!/usr/bin/python3

import os, sys
import subprocess
import yaml
import os.path as path
import time

# EXEC_DIR = path.dirname(path.abspath(__file__))

## parse config file
with open('./iperf.yml', 'r') as yml_fd:
    cfg = yaml.load(yml_fd)

hosts = cfg['hosts']
ASYNC = cfg['async']
offset = cfg['offset']

if offset > 0:
    time.sleep(offset * 60 + 60) # avoid iperf client test overlap 

proc_pool = []
iperf_cmd = "iperf  -c %s -p %d -t %d -P %d" 

log_fd = open('./iperf.log', 'a')
err_fd = open('./iperf.err', 'a')

for host in hosts:
    cmd = iperf_cmd % (
        host, 
        cfg['iperf_port'],
        cfg['iperf_time'],
        cfg['iperf_connection_num'])
    
    if ASYNC:
        log_fd.write("\n%s\n"%time.asctime())
        p = subprocess.Popen(cmd, stdout=log_fd, stderr=err_fd, shell=True)
        proc_pool.append(p)
    else:
        log_fd.write("\n%s\n"%time.asctime())
        subprocess.call(cmd, stdout=log_fd, stderr=err_fd, shell=True)

if ASYNC:
    for proc in proc_pool:
        proc.wait()

log_fd.close()
err_fd.close()
