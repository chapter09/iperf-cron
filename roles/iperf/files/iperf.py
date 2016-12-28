#!/usr/bin/python3

import os, sys
import subprocess
import yaml
import os.path as path

EXEC_DIR = path.dirname(path.abspath(__file__))

## parse config file
with open('./iperf.yml', 'r') as yml_fd:
    cfg = yaml.load(yml_fd)


hosts = []
ASYNC = cfg['async']


iperf_cmd = "iperf -c %s -p %d -t %d -P %d"

for host in hosts:
	if ASYNC:
		subprocess.Popen(, shell=True)
	else:
		subprocess.call()


if ASYNC:


