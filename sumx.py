"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr




class summ(gr.sync_block):
	def __init__(self):  # only default arguments here
		gr.sync_block.__init__(
        	self,
        	name='Sum',
        	in_sig=[np.float32],
        	out_sig=[np.float32],
        )
		self.valor = 0
		self.list_frq = (292000000,433920000,315000000)
		self.pos = 0
		self.detectada = 0


	def work(self, input_items, output_items):
		
		

		in_stream = input_items[0][:]
		if(len(in_stream)<128):
			return

		sum_ = sum(in_stream)
		if(sum_ >0):
			somar = np.log10(sum_/10)
			self.valor = somar
			size = len(in_stream)			
			self.consume(0,size)

		
		return len(output_items[0])
	def freq_detectada(self):
		if(self.detectada >0):
			return self.detectada
		else:
			return "Procurando..."
	def freq_ativa(self):
		if(self.valor > 1):
			self.detectada = self.list_frq[self.pos]
			return self.list_frq[self.pos]
		else:

			if(self.pos <= len(self.list_frq)-1):
				val = self.list_frq[self.pos]
				self.pos = self.pos +1
				return val

			else:
				self.pos = 0
				val = self.list_frq[0]
				return val


