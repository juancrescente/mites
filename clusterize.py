#!/usr/bin/env python
# coding: utf-8

import argparse
from subprocess import Popen, PIPE
import os
import pathlib
import shutil
import os
import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--families", help="Families dir", required=True)
parser.add_argument("--clusters", help="Clusters dir", required=True)
parser.add_argument("--csv", help="CSV clusters file", required=True)
parser.add_argument("--fasta", help="Fasta clusters file", required=True)
parser.add_argument("-g", "--genome", help="", required=True)
parser.add_argument("-i", "--pid", help="", default=0.96)
parser.add_argument("-m", "--min", help="Min elements in clusters", default=45, type=int)
parser.add_argument("-w", "--workers", help="Min elements in clusters", default=1)
args = parser.parse_args()

#list families and cluster them
files = [f for f in os.listdir(args.families) if os.path.isfile(os.path.join(args.families, f))]
count = 0
total = len(files)
for file in files:
    file_path = args.families + file
    
    count += 1
    print("%i / %i" % (count,total))
    c_dir = args.clusters + file + "/"
    if os.path.isdir(c_dir):
        shutil.rmtree(c_dir)
    pathlib.Path(c_dir).mkdir(parents=True, exist_ok=True)
    cmd_list = [
    './bin/vsearch-2.13.4/bin/vsearch',
    '--cluster_fast', file_path,
    '--threads',str(args.workers),
    '--strand','both',
    '--clusters', c_dir + "c_",
    '--iddef','1',
    '--id', str(args.pid)]
    p = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
    out,err = p.communicate()

#list cluster and filter by min number
files = [f for f in os.listdir(args.families) if os.path.isfile(os.path.join(args.families, f))]
count = 0
total = len(files)
res = {}
valid_clusters = {}
f = open(args.csv, 'w')
for file in files:
    file_path = args.families + file
    c_dir = args.clusters + file + "/"
    clusters = [f for f in os.listdir(c_dir) if os.path.isfile(os.path.join(c_dir, f))]
    seqs = []
    for cluster in clusters:
        file_c = open(c_dir + cluster, "r")
        count_seqs = 0
        for line in file_c:
            if line[0:1] == ">":
                count_seqs += 1
        seqs.append(count_seqs)
        if count_seqs > args.min:
            clus_file = c_dir + cluster
            f.write("%s,%s,%s,%s\n"%(file,clus_file,cluster,count_seqs))