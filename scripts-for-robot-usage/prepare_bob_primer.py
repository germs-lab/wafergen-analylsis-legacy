#!/usr/bin/python 
"""
This script generate two files "for_robot.csv", "for_record.tsv"
usage:
python prepare_bob_primer.py lan_list_target.txt bob_primer_plate.clean.tsv
"""

import sys


def replace_name(name):
    name = name.replace("01","1")
    name = name.replace("02","2")
    name = name.replace("03","3")
    name = name.replace("04","4")
    name = name.replace("05","5")
    name = name.replace("06","6")
    name = name.replace("07","7")
    name = name.replace("08","8")
    name = name.replace("09","9")
    return name

def get_loc(i):
    if i > 95:
        print "over one plate"
        return ""
    alpha = ["A","B","C","D","E","F","G","H"]
    num = ["1","2","3","4","5","6","7","8","9","10","11","12"]
    loc = alpha[i%8]+num[i/8]
    return loc

def main():
    replicate = 3
    #read list of target
    target = []
    for line in open(sys.argv[1],'r'):
        target.append(line.strip())

    #read primer location
    prim = {}



    for line in open(sys.argv[2],'r'):
        spl = line.strip().split('\t')
        tmp_name = spl[6].split('_')
        name = '_'.join(tmp_name[:-1])
        if prim.has_key(name):
            lo = replace_name(spl[5])
            prim[name].append([spl[0],lo,name])
        else:
            lo = replace_name(spl[5])
            prim[name] = [[spl[0],lo,name]]


    plate = {}
    for tar in target:

        if plate.has_key(prim[tar][0][0]):
            plate[prim[tar][0][0]].append(prim[tar])
        else:
            plate[prim[tar][0][0]] = [prim[tar]]

            #result = [pr[0],pr[1],"1","A1","2","1"]
            #print '\t'.join(result)

    order = 0
    repli = 0
    
    for_robot = open("for_robot.csv",'w')
    for_record = open("for_record.tsv",'w')
    result_robot = ["Rack", "Source", "Rack", "Destination", "Volume", "Tool"]
    for_robot.write(','.join(result_robot)+'\n')
    result = ["bob plate number", "robot source plate location","source location","target gene", "target location"]
    for_record.write('\t'.join(result)+'\n')

    k = 1
    for i in range(1,9):
        pla = "plate"+str(i)

        if plate.has_key(pla):
            item = plate[pla]
            
            
            result_robot = [str(k)]
            result = [pla,str(k)]
            for one_target in item:
                for j in range(0,replicate):
                    for one_primer in one_target:
                        result_robot.append(one_primer[1])
                        result.append(one_primer[1])
                        
                        result_robot.append("1")
                        result.append(one_primer[2])

                        result_robot.append(get_loc(order))
                        result.append(get_loc(order))

                        result_robot.append("2")

                        result_robot.append("1")


                        for_robot.write(','.join(result_robot)+'\n')
                        for_record.write('\t'.join(result)+'\n')
                        result_robot = [str(k)]
                        result = [pla,str(k)]
                    order += 1
            k += 1



if __name__ == '__main__':
    main()
