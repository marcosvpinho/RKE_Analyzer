"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
from __future__ import division
import numpy as np
from gnuradio import gr


class crossing(gr.basic_block):


    def __init__(self):  # only default arguments here
        gr.basic_block.__init__(
            self,
            name='crossing',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.count = 0
        self.fs = 180000
        

    def general_work(self, input_items, output_items):
        
        in_stream = input_items[0][:]
        #print(in_stream)
        zero_crossings = np.where(np.diff(np.signbit(input_items)))
        size = len(zero_crossings[1])
        zeros_ = []
        for x in range(0,size-2):
        	zeros_.append(zero_crossings[1][x+1] - zero_crossings[1][x])
        if (len(zeros_)):
            minimo = min(zeros_)
            valor = 1/(minimo/self.fs)
            print(valor)
        i0 = len(in_stream)
        self.consume(0, i0)
        #output_items[0][:] = np.zeros((size),dtype=np.float32)
        return len(output_items[0])

        






