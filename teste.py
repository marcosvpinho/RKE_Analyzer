"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
import numpy as np


def general_work(replacements, input_items, tam):
    size = len(input_items)
    if(size < tam):
        return 0

    max_length = max([len(before) for before, after in replacements] + [0])
    ii = 0
    oo = 0
    buffer_ = []
    while ii + max_length < len(input_items):

        for before, after in replacements:

            if np.all(input_items[ii : ii + len(before)] == before):

                buffer_.append(after)
                ii += len(before)

                oo += 1
                break
        else:
            buffer_.append(32)
            oo += 1
            ii += 1
    size_b = len(buffer_)
    flag = 0
    pos = 0
    seq = np.zeros((tam),dtype=np.int8)
    #print(buffer_)
    for i in range(0,size_b):
        if(buffer_[i] == 32 and flag == 0 ):
            flag = 1

        elif(buffer_[i]!= 32 and flag ==1):
            seq[pos] = buffer_[i]
            pos=pos+1
            if(pos==tam):
                flag=2
                print(seq)
            
        elif(flag == 2 and buffer_[i]==32):
            print(seq)
            return tam

        else:
            pos = 0
            seq = np.zeros((tam),dtype=np.int8)


    return oo

def main():
    packet = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1, 0,1,1, 0,0,1, 0,0,1, 0,0,1, 0,0,1, 0,0,1, 0,0,1, 0,0,1, 0,0,1, 0,0,1, 0,1,1, 0,1,1, 0,0,0, 0,1,1, 0,1,1, 0,1,1, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ,0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0)
    replacementsize = []
    replacements = []
    replacements.append([((0,0,0,0,0,0,0,0,1), 32), ((0,1,1), 48), ((0,0,1), 49)])
    replacements.append([((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 32),((0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1), 46),((0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0), 49),((0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0), 50)])
    

    replacementsize.append(12)
    replacementsize.append(9)    
    for x in range(0,2):
        general_work(replacements[x],packet,replacementsize[x])

if __name__ == "__main__":
    main()