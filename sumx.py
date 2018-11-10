"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr


class summ(gr.sync_block):
    def __init__(self, limiar_db=10.0):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Sum',
            in_sig=[np.float32],
            out_sig=[],
        )
        self.valor = 0
        self.list_frq = (292000000, 299000000, 315000000, 433920000)
        self.pos = 0
        self.limiar_db = limiar_db

    def work(self, input_items, output_items):
        in_stream = input_items[0][:]
        if len(in_stream) < 1024:
            return 0

        self.valor = 10*np.log10(sum(in_stream))
        # ~print(self.valor)
        self.consume(0, len(in_stream))

        return 0

    def freq_detectada(self):
        if self.valor > self.limiar_db:
            return self.list_frq[self.pos]
        else:
            return "So ruido..."

    def freq_ativa(self):
        if self.valor < self.limiar_db:
            self.pos += 1
            self.pos %= len(self.list_frq)
        print(self.list_frq[self.pos], self.valor, self.limiar_db)
        return self.list_frq[self.pos]