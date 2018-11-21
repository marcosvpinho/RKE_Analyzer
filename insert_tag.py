"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
import pmt
from gnuradio import gr


class clock_reset(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, sps=1):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Inserir tag',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.sps = sps
        self._last_called = 0

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        
        if self.nitems_written(0) - self._last_called > 1000000:
            key = pmt.intern('clock_est')
            print("enviandooo")
            value = pmt.to_pmt((0.1, self.sps))
            self.add_item_tag(0, self.nitems_written(0), key, value)
            self._last_called = self.nitems_written(0)
        output_items[0][:] = input_items[0] * 1.0
        return len(output_items[0])