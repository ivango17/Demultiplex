#!/bin/bash


#SBATCH --account=bgmp                    
#SBATCH --partition=compute               
#SBATCH --cpus-per-task=8                 
#SBATCH --mem=32GB                        

conda activate base

/usr/bin/time ./demultiplexing.py -R1 "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz" -R2 "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz" -R3 "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz" -R4 "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz" -od "./Demultiplex_Outputs" -osf "Summary_of_demultiplexing"

# 1294_S1_L008_R1_001.fastq.gz
# 1294_S1_L008_R2_001.fastq.gz
# 1294_S1_L008_R3_001.fastq.gz
# 1294_S1_L008_R4_001.fastq.gz