#!python

import os
import sys
import re
from collections import defaultdict
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def main(dstat_file_path, output_path):
    rdata = defaultdict(lambda: {})
    data = defaultdict(lambda: {})
    with open(dstat_file_path, 'r') as fhandle:
        for line in fhandle:
            if "CDT 2019" == line[-9:-1]:
                for key in data.keys():
                    rdata[key][line[-18:-10]] = data[key]
            elif not line.startswith("CONTAIN"):
                vals = line.split()
                data[vals[1]]['cpu%'] = float(re.findall(r"((\d+.)?\d+)", vals[2])[0][0])
                data[vals[1]]['mem'] = float(re.findall(r"((\d+.)?\d+)", vals[3])[0][0])
                data[vals[1]]['mem%'] = float(re.findall(r"((\d+.)?\d+)", vals[6])[0][0])
                data[vals[1]]['nw_ip'] = float(re.findall(r"((\d+.)?\d+)", vals[7])[0][0]) # there can be MB,kB,GB
                data[vals[1]]['nw_op'] = float(re.findall(r"((\d+.)?\d+)", vals[9])[0][0])
                data[vals[1]]['bk_ip'] = float(re.findall(r"((\d+.)?\d+)", vals[10])[0][0])
                data[vals[1]]['bk_op'] = float(re.findall(r"((\d+.)?\d+)", vals[12])[0][0])
    print(rdata)


if "__main__" == __name__:
    if not os.path.isfile(sys.argv[1]):
        raise 'Cannot find dstats file {}'.format(sys.argv[1])

    main(sys.argv[1], sys.argv[2])
