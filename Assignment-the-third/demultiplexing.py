#!/usr/bin/env python

import argparse
import gzip
import matplotlib.pyplot as plt
import numpy as np

complimentDict = {"A":"T", "T":"A", "C":"G", "G":"C", "N":"N"}
knownIndexes = {}
files = {}
indexHopped = {}
unknownCounter = 0
numCorrectPairs = 0
numIndexSwapping = 0
totReads = 0

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
            knownIndexes[line[4]] = 0

print(knownIndexes)

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
    totReads += 1
    R3_line2 = reverse_comp(R3_line2)

    currIndex = (R2_line2, R3_line2)

    # if currIndex not in indexCountDict:
    #     indexCountDict[currIndex] = 1
    # else:
    #     indexCountDict[currIndex] += 1

    if currIndex[0] == currIndex[1] and currIndex[0] in knownIndexes:
        files[currIndex[0]][0].write(f"{R1_line1}\t{currIndex[0]}-{currIndex[1]}\n{R1_line2}\n{R1_line3}\n{R1_line4}\n")
        files[currIndex[1]][1].write(f"{R4_line1}\t{currIndex[0]}-{currIndex[1]}\n{R4_line2}\n{R4_line3}\n{R4_line4}\n")
        knownIndexes[currIndex[0]] += 1
        numCorrectPairs += 1

    else:
        if currIndex[0] in knownIndexes and currIndex[1] in knownIndexes:
            fh_hopped_R1.write(f"{R1_line1}\t{currIndex[0]}-{currIndex[1]}\n{R1_line2}\n{R1_line3}\n{R1_line4}\n")
            fh_hopped_R2.write(f"{R4_line1}\t{currIndex[0]}-{currIndex[1]}\n{R4_line2}\n{R4_line3}\n{R4_line4}\n")
            numIndexSwapping += 1
            
            if currIndex in indexHopped:
                indexHopped[currIndex] += 1

            else:
                indexHopped[currIndex] = 1

        else:
            fh_unknown_R1.write(f"{R1_line1}\t{currIndex[0]}-{currIndex[1]}\n{R1_line2}\n{R1_line3}\n{R1_line4}\n")
            fh_unknown_R2.write(f"{R4_line1}\t{currIndex[0]}-{currIndex[1]}\n{R4_line2}\n{R4_line3}\n{R4_line4}\n")
            unknownCounter += 1



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


#Output file writing

with open(f"{outputDir}/{outputSummaryFile}", "w") as fh:
    fh.write("Summary Information for demultiplexing\n\n")

    fh.write(f"Total number of reads read {totReads}\n\n")

    fh.write(f"Number of matched reads: {numCorrectPairs}\n\n")

    fh.write(f"Number of unknown reads: {unknownCounter}\n\n")

    fh.write(f"Number of index swapping: {numIndexSwapping}\n\n")
    
    fh.write(f"Proportion of reads from each sample\n")
    fh.write(f"Index pair\tPercentage\n")

    for key in knownIndexes:
        percent = 100 * (knownIndexes[key] / numCorrectPairs)
        fh.write(f"{key}\t{percent}%\n")
    fh.write("\n")

    fh.write("Index Hopped Pairs and Counts\n")
    fh.write("Pairs\tCounts\n")

    for key in indexHopped:
        fh.write(f"{key}\t{indexHopped[key]}\n")

xaxis = []
yaxis = []

for key in knownIndexes:
    xaxis.append(key)
    yaxis.append(knownIndexes[key])

plt.title("Proportion of matched reads per index")
plt.xlabel("Index")
plt.ylabel("Count")

plt.bar(xaxis, yaxis, width=1, color="green")
plt.savefig("Index_Proportion.png")



    



