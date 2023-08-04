#!/usr/bin/env python

import matplotlib.pyplot as plt
import argparse
import numpy as np
import gzip

def get_args():
    parser = argparse.ArgumentParser(description="This program generates a histogram of Qscores for a FASTQ file.")
    parser.add_argument("-f", "--filename", help="What is the filepath for the file to be read", type=str)
    parser.add_argument("-o", "--outputfile", help="What do you want this file to be called", type=str)
    return parser.parse_args()

args = get_args()

file = args.filename
output = args.outputfile

def convert_phred(letter: str):
    '''Converts a single character into a phred score. Assumes scores are phred+33.'''
    return ord(letter) - 33

numReads = 0
j = 0
scores = []
xaxis = []
yaxis = []

with gzip.open(file, "rt") as fh:
    for line in fh:
        j += 1
        if j % 4 == 0:
            line = line.strip()
            numReads += 1
            for i in range(len(line)):
                
                if len(scores) != i:
                    scores[i] += convert_phred(line[i])
                else:
                    scores.append(convert_phred(line[i]))

for i in range(len(scores)):
    scores[i] /= numReads

for i in range(len(scores)):
    xaxis.append(i)
    yaxis.append(scores[i])

plt.title(f"Distribution of Phred Scores for {output}")
plt.xlabel("Seq position")
plt.ylabel("AVG phred score")

plt.bar(xaxis, yaxis, width=1, color="red")
plt.savefig(output)


