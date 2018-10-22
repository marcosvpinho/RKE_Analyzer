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
            name='crossing zero',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        self.count = 0
        self.fs = 180000
        self.sps = 0
        

    def general_work(self, input_items, output_items):
        
        in_stream = input_items[0][:]
        #print(in_stream)
        zero_crossings = np.where(np.diff(np.signbit(input_items)))
        size = len(zero_crossings[1])
        zeros_ = []
        for x in range(0,size-2):
            dif = zero_crossings[1][x+1] - zero_crossings[1][x]
            if dif > 10:
        	   zeros_.append(dif)

        if (len(zeros_)):
            minimo = min(zeros_)
            valor = 1/(minimo/self.fs)
            self.sps = self.fs/valor

        i0 = len(in_stream)
        self.consume(0, i0)
        #output_items[0][:1] = np.array(buffer_)
        return len(output_items[0])

        
    def retorna_sps(self):
        return self.sps

    def ativo(self):
        if(self.sps>1):
            return True
        else:
            return False






