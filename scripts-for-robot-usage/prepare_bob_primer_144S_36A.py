#!/usr/bin/python 
"""
This script generate two files "for_robot.csv", "for_record.tsv"
usage:
python prepare_bob_primer_144S_36A.py lan_list_target.txt bob_primer_plate.clean.tsv
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
    replicate = 1
    #no_use = ["G5", "H5","F6","G6","H6","G7","H7","F8","G8","H8"]
    no_use = ["B5","B6","B7","B8","C5","C6","C7","C8","D5","D6","D7","D8","E5","E6","E7","E8","F5","F6","F7","F8","G5","G6","G7","G8","H5","H6","H7","H8"]
    #no_use = []
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

                        val_loc = get_loc(order)
                        for loop in range(0,10):
                            if val_loc in no_use:
                                order += 1
                                val_loc = get_loc(order)
                            else:
                                break
                            
                        result_robot.append(one_primer[1])
                        result.append(one_primer[1])
                        
                        result_robot.append("1")
                        result.append(one_primer[2])

                        result_robot.append(val_loc)
                        result.append(val_loc)

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
