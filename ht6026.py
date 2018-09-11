"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr

class blk(gr.basic_block):
    def __init__(self, min_agreements=2, debug=True):  # only default arguments here
        gr.basic_block.__init__(
            self,
            name="ht6026",
            in_sig=[np.int8],
            out_sig=[np.int8])
        self.min_agreements = min_agreements
        self.debug = debug

        self.bit1 = np.array([0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1])
        self.bit0 = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])
        self.bit2 = np.array([0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0])

        self.agreements = 0
        self.buffer_ = []  

    def general_work(self, input_items, output_items):
        in_stream = input_items[0][:]
        nonzeros = np.flatnonzero(in_stream)
        if len(nonzeros) == 0:
            i0 = len(in_stream)
        else:
            i0 = nonzeros[0]
        # i0 = first nonzero input index.

        in_stream = in_stream[i0:]
        self.consume(0, i0)
        bit0= np.array([0])
        in_stream =  np.concatenate((bit0,in_stream),axis=None)
        

        if len(in_stream) < 352 or len(output_items[0]) < 10:
            return 0
            
        # At this point, the first entry should necessarily be 1, and
        # we should have at least 100 input data items.

        #in_stream = in_stream[1:]
        #self.consume(0, 1)
        
        buffer_ = []
        while len(in_stream) >= 16 and len(buffer_) < 9:        

            seq3, in_stream = in_stream[:16], in_stream[16:]
            self.consume(0, 16)
            if np.all(seq3 == self.bit0):
                buffer_.append(0)
                
            elif np.all(seq3 == self.bit1):
                buffer_.append(1)
                
            elif np.all(seq3 == self.bit2):
                buffer_.append(2)    
                
            else:
                self.consume(0, 16 * (9 - len(buffer_)))
                return 0

        if buffer_ == self.buffer_:
            self.agreements += 1
        else:
            self.buffer_ = buffer_
            self.agreements = 0

        if self.agreements > self.min_agreements:
            output_items[0][:9] = np.array(buffer_) + ord('0')
            output_items[0][9] = ord('\n')
            if self.debug:
                print(self.agreements, buffer_)
            return 10
        else:
            return 0
