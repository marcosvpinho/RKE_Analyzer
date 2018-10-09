"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr

class blk_cod(gr.basic_block):
    def __init__(self, debug=True):  # only default arguments here
        gr.basic_block.__init__(
            self,
            name="ht6026",
            in_sig=[np.int8],
            out_sig=[np.int8])

        self.sync = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.bit1 = np.array([0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1])
        self.bit0 = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])
        self.bit2 = np.array([0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0])

    def general_work(self, input_items, output_items):
        in_stream = input_items[0][:]
        if len(in_stream) < 16:
            return 0
        
        buffer_ = []     

        seq3, in_stream = in_stream[:16], in_stream[16:]
        while(true):
            if np.all(seq3 == self.sync):
                buffer_.append(5)
                output_items[0][:1] = np.array(buffer_)
                self.consume(0,16)
                return len(output_items[0])

            else:
                if np.all(seq3 == self.bit0):
                    buffer_.append(0)
                    output_items[0][:1] = np.array(buffer_)
                    self.consume(0,16)
                    return len(output_items[0])
                    
                elif np.all(seq3 == self.bit1):
                    buffer_.append(1)
                    output_items[0][:1] = np.array(buffer_)
                    self.consume(0,16)
                    return len(output_items[0])
                    
                elif np.all(seq3 == self.bit2):
                    buffer_.append(2) 
                    output_items[0][:1] = np.array(buffer_)
                    self.consume(0,16)
                    return len(output_items[0])

                else:
                    in_stream = in_stream[1:]
                    seq3= in_stream[:16]
                    self.consume(0, 1)

                    if (len(in_stream))<16:
                        return 0
