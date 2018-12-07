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

    def __init__(self,sample_rate=1.0e6, threshold = 20):  # only default arguments here
        gr.basic_block.__init__(
            self,
            name='Zero Crossing',
            in_sig=[np.float32],
            out_sig=[]
        )
        self.count = 0
        self.threshold = threshold
        self.fs = sample_rate
        self.sps = 0
        self.flag = False
        self.pos = 0

    def general_work(self, input_items, output_items):
        in_stream = input_items[0]
        if(len(in_stream)<1000):
            return 0
        ## cruzamentos por zero
        in_stream = in_stream[:1000]
        zero_crossings = np.where(np.diff(np.signbit(input_items)))
        size = len(zero_crossings[1])
        zeros_ = []
        zeros_ativo = []

        for x in range(0,size-2):
            dif = zero_crossings[1][x+1] - zero_crossings[1][x]
            #pegando apenas diferencas maiores que 5 amostras
            zeros_ativo.append(dif) 
            if dif > self.threshold:
               zeros_.append(dif)

        ## pegando o menor valor
        if (len(zeros_)):
            minimo = min(zeros_)
            valor = 1/(minimo/self.fs)
            self.sps = self.fs/valor
        else:
            self.sps = 0


        #i0 = len(in_stream)
        self.consume(0, 1000)
        #output_items[0][:1] = np.array(buffer_)
        return 0
        
    def retorna_sps(self):
        if(self.sps < self.threshold):
            return 5
        else:
            return int(self.sps)


    def retorna_freq(self):
        if(self.sps > self.threshold):
            return int(self.fs/self.sps)
        else:
            return 0
