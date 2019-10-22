#!/usr/bin/python
#This file converts the transcript range into genomic range
#This files requies alignment data along with file with query ranges
def main():  
    file1 = open("file1","r")
    f1 = file1.readlines()
    D = {}
    import re
    for x1 in f1:
        y1 = re.search("(^TR\d+)\t(CHR\d+)\t(\d+)\t(.+)", x1)
        if y1:
            D.update( {(y1.group(1)) : [(y1.group(2)),(y1.group(3)),(y1.group(4))]} )
    file4 = open("file4","r")
    file_out = open("result","w+")
    f2 = file4.readlines()
    for x2 in f2:
        y2 = re.search("(^TR\d+)\t(\d+)\t(\d+)", x2)
        x2 = x2[:-1]
        val_g = 0
        val_t = 0
        if (y2.group(1)) in D:
            valg = D[(y2.group(1))][1]
            val_g = int(valg)
            valt1 = (y2.group(2))
            val_t1 = int(valt1)
            valt2 = (y2.group(3))
            val_t2 = int(valt2)
            cigar = D[(y2.group(1))][2]
        pattern = re.compile(r'([0-9]+)([MIDNSHPX=])')
        seq = ''
        for (numbers, letter) in re.findall(pattern, cigar):
            numbers = int(numbers)
            seq = seq + (numbers * letter)
        seq = str(seq)
        count = 0
        t1_count = 0
        t2_count = 0
        g1_count = 0
        g2_count = 0
        Se = {'M':1, 'I':1, 'S':1, '=':1,'X':'1'}
        Re = {'M':1, 'D':1, 'N':1, '=':1,'X':'1'}
        for op in seq:
            count += 1
            if op in Se:
                t2_count += 1
                if (t1_count <= val_t1):
                    t1_count += 1
            if t2_count > val_t2:
                    break
            if op in Re:
                g2_count += 1
                if (t1_count <= val_t1):
                    g1_count += 1
        total1 = val_g + g1_count
        total2 = val_g + g2_count
        st = D[(y2.group(1))][0]
        print ('{0}\t{1}\t{2}\t{3}\n'.format(x2, st, total1, total2))
main()

