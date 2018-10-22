import numpy as np
from gnuradio import gr

class blkht6026(gr.basic_block):
    def __init__(self):  # only default arguments here
        gr.basic_block.__init__(
            self,
            name='My Replacement0',
            in_sig=[np.int8],
            out_sig=[np.int8]
        )
        #self.replacements = [((0,0,0,0,0,0,0,1), 32), ((0,1,1), 48), ((0,0,1), 49)]
        self.replacements =[((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 32),((0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1), 46),((0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0), 49),((0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0), 50)]


    def general_work(self, input_items, output_items):

        if(len(input_items[0]) < 300):
            return 0
        max_length = max([len(before) for before, after in self.replacements] + [0])
        ii = 0
        oo = 0
        buffer_ = []
        while ii + max_length < len(input_items[0]):
            for before, after in self.replacements:
                if np.all(input_items[0][ii : ii + len(before)] == before):
                    #output_items[0][oo] = after
                    buffer_.append(after)
                    ii += len(before)

                    oo += 1
                    break
            else:
                ii += 1
        output_items[0][:len(buffer_)] = np.array(buffer_)
        print("ht6026:", output_items[0])
        self.consume(0, ii)
        return oo