#!/usr/bin/python3

import csv 
import os, sys
import time
import re
from datetime import datetime
from argparse import ArgumentParser

time_pt = r'\d{2}:\d{2}:\d{2}'
host_pt = r'Client connecting to\s*(.*), TCP port (\d*)'
bw_pt = r'\[SUM\]\s*.*MBytes\s*(\d+\.?\d*)\s*Mbits/sec'


def parse_args():
    parser = ArgumentParser(usage="iperf-log-parser.py [options]")
    parser.add_argument("-p", dest="path", default="../logs/", 
                        help="Path to log files")
    opts = parser.parse_args()
    return opts


def parse(fp):
    record_dict = {}
    hosts = set()
    with open(fp, encoding='ISO-8859-1') as fd:
        t = None
        for line in fd.readlines():
            try:
                if re.search(time_pt, line):
                    # time
                    t = datetime.strptime(line.strip(), '%c').strftime('%m-%d %H:00')
                    record_dict[t] = {}
                    continue
                if re.search(host_pt, line) and t:
                    # host
                    h = re.match(host_pt, line).groups()[0]
                    hosts.add(h)
                    record_dict[t][h] = 0
                    continue
                if re.search(bw_pt, line) and t:
                    # bandwidth
                    bw = re.match(bw_pt, line).groups()[0]
                    record_dict[t][h] = float(bw)
                    continue
            except ValueError as e:
                print(e)
                print(fp, line, t)

    
    with open(os.path.splitext(fp)[0]+'.csv', 'w', newline='') as csvfile:
        wt = csv.writer(csvfile) 
        wt.writerow(['time'] + list(hosts))
        try:
            for t in record_dict:
                wt.writerow([t] + 
                            [record_dict[t][h] 
                             if record_dict[t].get(h) is not None 
                             else 0 for h in hosts])
        except ValueError as e:
            print(e)
            print(fp, t, h)


    
if __name__ == '__main__':
    opts = parse_args()
    for f in os.listdir(opts.path):
        if os.path.splitext(f)[1] != ".log":
            continue
        parse(os.path.join(opts.path, f))

