#! /user/bin/python -O
# Jason Matthew Torres
'''
Python 3.5.0 script for merging atac peaks with bedtools
Usage:
module add bedtools
python script
'''

import os,sys,gzip,re
import subprocess as sp
import numpy

work_dir = "/well/mccarthy/users/jason/projects/atac_analyses/evaluate_peaks/"
peak_dir = "/well/mccarthy/production/atac-seq/data/human_islets/full_merged_data/peaks/"
elife_file = "/well/mccarthy/users/jason/projects/atac_analyses/elife_samples_names_for_jason.txt"
out_dir = work_dir + "eLife2018/"
out_file = out_dir + "merged_peaks.txt"
suffix = ".tn5.pval0.01.300K.bfilt.narrowPeak.gz"

def get_elife_list():
    fin = open(elife_file,'r')
    lst = []
    for l in fin:
        lst.append(l.strip())
    fin.close()
    return lst

def combine_and_sort():
    elife_list = get_elife_list()
    elife_list.append("HP1535")
    elife_list.append("HP1507_CMRL")
    print(elife_list)
    fout = open(out_dir+"temp.bed",'w')
    for f in elife_list:
        fname = peak_dir + f + suffix
        if os.path.isfile(fname) == True:
            sys.stdout.write(f+"\n")
            #norm_file = out_dir+f+".narrowPeak"
            #norm_list.append(norm_file)
            fin = gzip.open(fname,'rb')
            for line in fin:
                l = line.strip().split()
                write_list = [re.sub("b","",re.sub("'","",str(l[0]))),
                              re.sub("b","",re.sub("'","",str(l[1]))),
                              re.sub("b","",re.sub("'","",str(l[2])))]

                fout.write("\t".join(write_list)+"\n")
            fin.close()
    fout.close()
    command = "sort -k1,1 -k2,2n " +  out_dir + "temp.bed" + " | uniq -u " " > " + out_dir + "temp.sorted.bed"
    sp.check_call(command,shell=True)

def merge_bed_file(outname):
    print("Merging peaks")
    command = "bedtools merge " + out_dir + "temp.sorted.bed" " > " + outname
    sp.check_call(command,shell=True)

def main():
    #combine_and_sort()
    merge_bed_file(out_file)


if (__name__=="__main__"): main()
