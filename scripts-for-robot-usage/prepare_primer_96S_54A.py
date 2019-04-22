#!/usr/bin/python 
"""
This script generate two files "for_robot.csv", "for_record.tsv"
usage:
python python wafergen/prepare_primer_96S_54A.py 54assays_primer_list.csv full_primer_location.csv 
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
    primer_volume = "2"
    well_position = 2
    sequence_name = 3
    plate_location = 0

    no_use = ["G5", "H5","F6","G6","H6","G7","H7","F8","G8","H8"]
    #no_use = ["B5","B6","B7","B8","C5","C6","C7","C8","D5","D6","D7","D8","E5","E6","E7","E8","F5","F6","F7","F8","G5","G6","G7","G8","H5","H6","H7","H8"]
    #no_use = []
    #read list of target
    target = []
    for n,line in enumerate(open(sys.argv[1],'r')):
        if n == 0:
            continue
        spl = line.strip().split(',')
        target.append(spl)


    #read primer location
    prim = {}
    for line in open(sys.argv[2],'r'):
        spl = line.strip().split(',')
        name = spl[sequence_name].strip()
        plate_loc = spl[plate_location]
        if prim.has_key(name):
            lo = replace_name(spl[well_position])
            prim[name].append([plate_loc,lo,name])
        else:
            lo = replace_name(spl[well_position])
            prim[name] = [plate_loc,lo,name]
            

    

    for_record = open("for_record.tsv",'w')
    result = ["plate number", "robot source plate location","source location","target gene", "target location"]
    for_record.write('\t'.join(result)+'\n')


    plate_observed = {}
    order = 0

    save_result_robot = {}
    plate_num_observed = []

    
    for tar in target:
      #  print tar
        val_loc = get_loc(order)
        for loop in range(0,10):
            if val_loc in no_use:
                order += 1
                val_loc = get_loc(order)
            else:
                break

        f_prim = prim[tar[1].strip()]

        plate = f_prim[0]
        if not plate_observed.has_key(plate):
            plate_observed[plate] = len(plate_observed)+1

        plate_num = str(plate_observed[plate])

        result_record = [f_prim[0],plate_num,val_loc,tar[0],f_prim[1]]
        result_robot = [plate_num, f_prim[1], "1", val_loc, primer_volume, "1"]
     #   print result_record
     #   print result_robot
        tmp = save_result_robot.get(result_robot[0],[])
        tmp.append([result_robot,result_record])
        save_result_robot[result_robot[0]] = tmp

        if not result_robot[0] in plate_num_observed:
            plate_num_observed.append(result_robot[0])

        r_prim = prim[tar[3].strip()]
        plate = r_prim[0]
        if not plate_observed.has_key(plate):
            plate_observed[plate] = len(plate_observed)+1

        plate_num = str(plate_observed[plate])

        result_record = [r_prim[0],plate_num,val_loc,tar[0],r_prim[1]]
        result_robot = [plate_num, r_prim[1], "1", val_loc, primer_volume, "1\
"]


   #     print result_record
   #     print result_robot

        tmp = save_result_robot.get(result_robot[0],[])
        tmp.append([result_robot,result_record])
        save_result_robot[result_robot[0]] = tmp
        if not result_robot[0] in plate_num_observed:
            plate_num_observed.append(result_robot[0])

        order += 1
   


    num_item = 0
    num_file = 1
    file_name = ""
    for plate_num in plate_num_observed:
        item = save_result_robot[plate_num]
    #    print num_item % 4
        if num_item % 4 == 0:
            file_name = "for_robot"+str(num_file)+".csv"
            for_robot = open(file_name,'w')
            result_robot = ["Rack", "Source", "Rack", "Destination", "Volume", "Tool"]
            for_robot.write(','.join(result_robot)+'\n')
            num_file += 1
            
        for re in item:

            re[0][0] = str(num_item % 4 + 1)
            re[1].append(str(num_item % 4 + 1))
            re[1].append(file_name)
            for_robot.write(','.join(re[0])+'\n')
            for_record.write('\t'.join(re[1])+'\n')

        num_item += 1
        

if __name__ == '__main__':
    main()
