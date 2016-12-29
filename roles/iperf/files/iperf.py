#!/usr/bin/python3

import os, sys
import subprocess
import yaml
import os.path as path

EXEC_DIR = path.dirname(path.abspath(__file__))

## parse config file
with open('./iperf.yml', 'r') as yml_fd:
    cfg = yaml.load(yml_fd)

hosts = cfg['hosts']
ASYNC = cfg['async']

iperf_cmd = "iperf  -c %s -p %d -t %d -P %d" 

for host in hosts:
	cmd = iperf_cmd % (
			host, 
			cfg['iperf_port'],
			cfg['iperf_time'],
			cfg['iperf_connection_num'])
	if ASYNC:
		subprocess.Popen(cmd, shell=True)
	else:
		subprocess.call(cmd, shell=True)


if ASYNC:


