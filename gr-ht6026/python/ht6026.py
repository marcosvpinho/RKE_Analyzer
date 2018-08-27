#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
from gnuradio import gr

class ht6026(gr.sync_block):


    def __init__(self, min_agreements=1, debug=True):
        gr.sync_block.__init__(self,
            name="ht6026",
            in_sig=[np.int8],
            out_sig=[np.int8])
        self.min_agreements = min_agreements
        self.debug = debug

        self.bit0 = np.array([0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1])
        self.bit1 = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])
        self.bit2 = np.array([0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0])

        self.agreements = 0
        self.buffer_ = []  


    def work(self, input_items, output_items):
        
        in_stream = input_items[0][:]
        nonzeros = np.flatnonzero(in_stream)
        if len(nonzeros) == 0:
            i0 = len(in_stream)
        else:
            i0 = nonzeros[0]
        # i0 = first nonzero input index.

        in_stream = in_stream[i0-1:]
        self.consume(0, i0-1)

        if len(in_stream) < 100 or len(output_items[0]) < 9:
            return 0

        # At this point, the first entry should necessarily be 1, and
        # we should have at least 100 input data items.

        in_stream = in_stream[0:]
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
                self.consume(0, 16 * (15 - len(buffer_)))
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

