"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr

class divide(gr.sync_block):
	def __init__(self):  # only default arguments here
		gr.sync_block.__init__(
        	self,
        	name='Divide',
        	in_sig=[np.float32],
        	out_sig=[np.float32],
        )
		self.maximum = 0.0
		self.flag = 0.0


	def work(self, input_items, output_items):
		
		
		in_stream = input_items[0][:]
		size = np.shape(in_stream)[0]
		self.maximum = np.maximum.reduce(in_stream)
		if(self.maximum < 0.05):
			output_items[0][:] = np.zeros((size),dtype=np.float32)				
			self.consume(0,size)
			return len(output_items[0])
		#	self.maximum = 0.1
		#print(in_stream)
		#print(self.maximum)
		out = np.zeros((size),dtype=np.float32)
		for i in range(0,size):

			out[i]=in_stream[i]/self.maximum

			

		
		output_items[0][:] = out[:]

		return len(output_items[0])


	def retorna_maximo(self):
		return self.maximum
