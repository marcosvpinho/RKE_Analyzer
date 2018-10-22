from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import numpy as np


class blkht6026(gr.basic_block):
    def __init__(self):  # only default arguments here
        gr.basic_block.__init__(
            self,
            name='My Replacement0',
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        #self.replacements = [((0,0,0,0,0,0,0,1), 32), ((0,1,1), 48), ((0,0,1), 49)]
        self.replacements =[((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 32),((0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1), 46),((0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0), 49),((0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0), 50)]


    def general_work(self, input_items, output_items):
        taps = np.ones(40)/(40)
        
        x = filter.fir_filter_fff(1, taps)
        x.declare_sample_delay(0)
        output_items = input_items*x