# Demultiplexing

## [demultiplexing.py](./demultiplexing.py)
This script takes five files from paired-end sequencing:
- **R1**: Sequence file for read 1
- **R2**: Index file respective to R1
- **R3**: Index file respective to R4
- **R4**: Sequence file for read 2
- **Index**: TSV file containing index names and sequences

The script also takes an argument for an output file to be generated containing summary information about the sample including proportion of reads for each index and a histogram showing read counts (eg. [Summary_of_Demultiplexing](./Assignment-the-third/Summary_of_Depultiplexing.md) and [Index_Proportion.png](./Assignment-the-third/Index_Proportion.png)).

#### Required Packages
- gzip
- argparse
- matplotlib.pyplot
- numpy

## [fastq_qscore_distribution.py](./fastq_qscore_distribution.py)
This script takes a FASTQ file and generates a bar graph of average quality scores in the file by position. Examples of this script's outputs can be found in [Graphs](./Graphs/).

The script only requires two files:
- **Input File**: FASTQ file to be processed
- **Output File**: Destination for png file

#### Required Packages
- gzip
- argparse
- matplotlib.pyplot
- numpy

## [Assignment the First](Assignment-the-first)
Due Saturday, July 29, 2023, 10:00 AM PDT.

## [Assignment the Second](Assignment-the-second)
Due on Monday, July 31, 2023, 10:00 AM PDT.

## [Assignment the Third](Assignment-the-third)
Due on Friday, August 11, 2023, 11:59 PM PDT.
