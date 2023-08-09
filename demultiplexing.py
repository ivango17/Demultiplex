#!/usr/bin/env python

import argparse
import gzip

complimentDict = {"A":"T", "T":"A", "C":"G", "G":"C"}
knownIndexes = {}
files = {}
indexCountDict = {}

def get_args():
    parser = argparse.ArgumentParser(description="This program demultiplexes Illumoina sequencing files.")
    parser.add_argument("-R1", "--R1", help="input fastq R1", type=str)
    parser.add_argument("-R2", "--R2", help="input fastq R1", type=str)
    parser.add_argument("-R3", "--R3", help="input fastq R1", type=str)
    parser.add_argument("-R4", "--R4", help="input fastq R1", type=str)
    parser.add_argument("-od", "--outputdir", help="Where will the output files be saved", type=str)
    parser.add_argument("-osf", "--outputsummary", help="What will the summary file be called", type=str)
    return parser.parse_args()

args = get_args()
R1 = gzip.open(args.R1, "rt")
R2 = gzip.open(args.R2, "rt")
R3 = gzip.open(args.R3, "rt")
R4 = gzip.open(args.R4, "rt")
outputDir = args.outputdir
outputSummaryFile = args.outputsummary

def reverse_comp(seq: str):
    '''This function takes a sequence as a string and returns the reverse compliment of that sequence.'''
    rcseq = ""
    rseq = seq[::-1]
    for i in range(len(seq)):
        rcseq += complimentDict[rseq[i]]
    return rcseq

#This generates a dictionary with the known indexes

# with open("./TEST-input_FASTQ/indexs.tsv") as fh:
#     for line in fh:
#         line = line.strip('\n')
#         line = line.split()
#         if line[0] != "sample":
#             knownIndexes[line[1]] = line[0]

with open("/projects/bgmp/shared/2017_sequencing/indexes.txt") as fh:
    for line in fh:
        line = line.strip('\n')
        line = line.split()
        if line[0] != "sample":
            knownIndexes[line[4]] = line[3]

for key in knownIndexes:
        fh_R1 = open(f"{outputDir}/{key}_R1.fq", "w")
        fh_R2 = open(f"{outputDir}/{key}_R2.fq", "w")
        files[key] = [fh_R1, fh_R2]

fh_hopped_R1 = open(f"{outputDir}/index_hopped_R1.fq", "w")
fh_hopped_R2 = open(f"{outputDir}/index_hopped_R2.fq", "w")
fh_unknown_R1 = open(f"{outputDir}/unknown_index_R1.fq", "w")
fh_unknown_R2 = open(f"{outputDir}/unknown_index_R2.fq", "w")


while True:

    R1_line1 = R1.readline().strip()
    R1_line2 = R1.readline().strip()
    R1_line3 = R1.readline().strip()
    R1_line4 = R1.readline().strip()

    R2_line1 = R2.readline().strip()
    R2_line2 = R2.readline().strip()
    R2_line3 = R2.readline().strip()
    R2_line4 = R2.readline().strip()

    R3_line1 = R3.readline().strip()
    R3_line2 = R3.readline().strip()
    R3_line3 = R3.readline().strip()
    R3_line4 = R3.readline().strip()

    R4_line1 = R4.readline().strip()
    R4_line2 = R4.readline().strip()
    R4_line3 = R4.readline().strip()
    R4_line4 = R4.readline().strip()

    if R1_line1 == "":
        break
    
    R3_line2 = reverse_comp(R3_line2)

    currIndex = (R2_line2, R3_line2)

    if currIndex not in indexCountDict:
        indexCountDict[currIndex] = 1
    else:
        indexCountDict[currIndex] += 1

    if currIndex[0] == currIndex[1] and knownIndexes[currIndex[0]]:
        files[currIndex][0].write(f"{R1_line1}\t{currIndex[0]}-{currIndex[1]}\n{R1_line2}\n{R1_line3}\n{R1_line4}\n")
        files[currIndex][1].write(f"{R4_line1}\t{currIndex[0]}-{currIndex[1]}\n{R4_line2}\n{R4_line3}\n{R4_line4}\n")

    else:
        if currIndex[0] in knownIndexes and currIndex[1] in knownIndexes:
            fh_hopped_R1.write(f"{R1_line1}\t{currIndex[0]}-{currIndex[1]}\n{R1_line2}\n{R1_line3}\n{R1_line4}\n")
            fh_hopped_R2.write(f"{R4_line1}\t{currIndex[0]}-{currIndex[1]}\n{R4_line2}\n{R4_line3}\n{R4_line4}\n")

        else:
            fh_unknown_R1.write(f"{R1_line1}\t{currIndex[0]}-{currIndex[1]}\n{R1_line2}\n{R1_line3}\n{R1_line4}\n")
            fh_unknown_R2.write(f"{R4_line1}\t{currIndex[0]}-{currIndex[1]}\n{R4_line2}\n{R4_line3}\n{R4_line4}\n")



#The below three blocks of statements close all of the output files and read files
for key in files:
    files[key][0].close()
    files[key][1].close()

fh_hopped_R1.close()
fh_hopped_R2.close()
fh_unknown_R1.close()
fh_unknown_R2.close()

R1.close()
R2.close()
R3.close()
R4.close()

with open(f"{outputDir}/{outputSummaryFile}", "w") as fh:
    for key in indexCountDict:
        fh.write(f"{key}\t{indexCountDict[key]}\n")



