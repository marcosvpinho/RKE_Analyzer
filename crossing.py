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
        self.ativo = 0
        self.flag = False
        self.list_frq = [292000000,433920000]
        self.pos = 0

    def general_work(self, input_items, output_items):
        in_stream = input_items[0][:]
        ## cruzamentos por zero
        zero_crossings = np.where(np.diff(np.signbit(input_items)))
        size = len(zero_crossings[1])
        zeros_ = []
        zeros_ativo = []

        for x in range(0,size-2):
            dif = zero_crossings[1][x+1] - zero_crossings[1][x]
            #pegando apenas diferencas maiores que 5 amostras
            zeros_ativo.append(dif) 
            if dif > 20:
        	   zeros_.append(dif)

        ## pegando o menor valor
        if (len(zeros_)):
            minimo = min(zeros_)
            valor = 1/(minimo/self.fs)
            self.sps = self.fs/valor
        else:
            self.sps = 0

        if (len(zeros_ativo)):
            minimo = min(zeros_ativo)
            valor = 1/(minimo/self.fs)
            self.ativo = self.fs/valor
        else:
            self.ativo = 0


        i0 = len(in_stream)
        self.consume(0, i0)
        #output_items[0][:1] = np.array(buffer_)
        return len(output_items[0])

        
    def retorna_sps(self):
        if(self.sps < 10):
            return 10
        else:
            return int(self.sps)

    def ativo(self):
        if(self.ativo>30):
            return True
        else:
            return False

    def freq(self):

        if(crossing.ativo(self)):
            return self.list_frq[self.pos]
        else:
            
            if(self.pos <= len(self.list_frq)-1):
                val = self.list_frq[self.pos]
                self.pos = self.pos +1
                return val

            else:
                self.pos = 0
                val = self.list_frq[self.pos]
                return val
