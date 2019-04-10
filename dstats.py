#!python

import os
import sys
import re
from collections import defaultdict, OrderedDict
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


def main(dstat_file_path, output_path):
    rdata = []
    data = defaultdict(lambda: defaultdict(lambda: []))
    with open(dstat_file_path, 'r') as fhandle:
        for line in fhandle:
            if "CDT 2019" == line[-9:-1]:
                rdata.append(line[-18:-10])
            elif not line.startswith("CONTAIN"):
                vals = line.split()
                data[vals[1]]['cpu%'].append(float(re.findall(r"((\d+.)?\d+)", vals[2])[0][0]))
                data[vals[1]]['mem'].append(float(re.findall(r"((\d+.)?\d+)", vals[3])[0][0]))
                data[vals[1]]['mem%'].append(float(re.findall(r"((\d+.)?\d+)", vals[6])[0][0]))
                data[vals[1]]['nw_ip'].append(float(re.findall(r"((\d+.)?\d+)", vals[7])[0][0])) # there can be MB,kB,GB
                data[vals[1]]['nw_op'].append(float(re.findall(r"((\d+.)?\d+)", vals[9])[0][0]))
                data[vals[1]]['bk_ip'].append(float(re.findall(r"((\d+.)?\d+)", vals[10])[0][0]))
                data[vals[1]]['bk_op'].append(float(re.findall(r"((\d+.)?\d+)", vals[12])[0][0]))

    ordata = rdata
    odata = data
    samples_per_min = 22
    samples_per_group = samples_per_min * 30
    tsize = len(ordata)

    for start in range(0,tsize, samples_per_group):
        end = start+samples_per_group
        if end > tsize:
            end = tsize
        size = len(rdata[start:end])

        xticks = range(0, size, size/30)
        # print(xticks, start,end,size)
        xticks_labels = [rdata[i] for i in range(start, end, size/30)]
        # print(xticks_labels)

        # lets draw diagram
        plt_idx = 1
        num_plots = 2 # cpu.mem%, mem
        fig = plt.figure()
        fig.set_figheight(num_plots * 4)
        plt.clf()
        plt.subplots_adjust(wspace=1, hspace=1)

        # cpu%
        plt.subplot(num_plots, 1, plt_idx)
        plt.xticks(xticks, xticks_labels, rotation='vertical')
        plt.yticks(range(0,100, 10), range(0,100, 10))
        # plt.ylim(bottom=0, top=100)
        plt.plot(range(size), data['containers_autopass_1']['cpu%'][start:end], label="autopass")
        plt.plot(range(size), data['containers_director_1']['cpu%'][start:end], label="director")
        plt.plot(range(size), data['containers_api_1']['cpu%'][start:end], label="api")
        plt.plot(range(size), data['containers_db_1']['cpu%'][start:end], label="db")
        plt.plot(range(size), data['containers_broker_1']['cpu%'][start:end], label="broker")
        plt.xlabel('time')
        plt.ylabel('% usage')
        plt.title('CPU Usage')
        lg = plt.legend(frameon=False)
        lg_txts = lg.get_texts()
        plt.setp(lg_txts, fontsize=10)
        plt_idx += 1

        # mem%
        plt.subplot(num_plots, 1, plt_idx)
        plt.xticks(xticks, xticks_labels, rotation='vertical')
        # plt.ylim(bottom=0, top=100)
        plt.plot(range(size), data['containers_autopass_1']['mem%'][start:end], label="autopass")
        plt.plot(range(size), data['containers_director_1']['mem%'][start:end], label="director")
        plt.plot(range(size), data['containers_api_1']['mem%'][start:end], label="api")
        plt.plot(range(size), data['containers_db_1']['mem%'][start:end], label="db")
        plt.plot(range(size), data['containers_broker_1']['mem%'][start:end], label="broker")
        plt.xlabel('time')
        plt.ylabel('% usage')
        plt.title('Percentation of Memory Used')
        lg = plt.legend(frameon=False)
        lg_txts = lg.get_texts()
        plt.setp(lg_txts, fontsize=10)
        plt_idx += 1

        fig.tight_layout()
        fig.savefig("{}_{}.png".format(output_path,start))
        plt.close(fig)


if "__main__" == __name__:
    if not os.path.isfile(sys.argv[1]):
        raise 'Cannot find dstats file {}'.format(sys.argv[1])

    main(sys.argv[1], sys.argv[2])
