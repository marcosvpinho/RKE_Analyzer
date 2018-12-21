import numpy as np
from gnuradio import gr

class blkfinal(gr.basic_block):
    def __init__(self,decoders_list = None,decoders_length = None):  # only default arguments here
        gr.basic_block.__init__(
            self,
            name='Decoder',
            in_sig=[np.int8],
            out_sig=[]
        )
        self.buffer_ = []
        self.codificador = "Nao Detectado"
        self.seq = []
        self.replacements = []
        self.replacementsize = []
        self.packet = []
        self.replacements = decoders_list
        self.replacementsize = decoders_length
        self.count = 0
        self.tamanho = 1



    def retorna_sequencia_detectada(self):
		if(self.count>0):
			return self.seq
		else:
			return "..."

        

    def retorna_codificador_detectado(self):
        return self.codificador

    def retorna_tam(self):
        return self.tamanho

    def replacement(self,replacements, input_items,tam):

		# print("replacements",replacements)
		# print("tamanho",tam)

		#print(input_items)
		max_length = max([len(before) for before, after in replacements] + [0])
		size = len(input_items)
		if(size < max_length):
			return 0
		ii = 0
		oo = 0
		buffer_ = []
		while ii + max_length < len(input_items):
			for before, after in replacements:
				#print(input_items[ii : ii + len(before)],"-------------",before)
				if np.all(input_items[ii : ii + len(before)] == before):
					buffer_.append(after)
					ii += len(before)
					oo += 1
					break
			else:
				buffer_.append('E')
				oo += 1
				ii += 1
		size_b = len(buffer_)
		flag = 0
		pos = 0
		seq = []
		for i in range(0,size_b):
			if(buffer_[i] == 'P' and flag == 0 ):
				flag = 1

			elif(buffer_[i]!= 'P' and buffer_[i]!= 'E' and flag ==1):
				#seq[pos] = buffer_[i]
				seq.append(buffer_[i])
				pos=pos+1
				if(pos==tam):
					flag=2

			elif(flag == 2 and (buffer_[i]=='E' or buffer_[i]=='P')):
				self.seq = seq[:]
				return tam
			else:
				pos  = 0
				flag = 0
				del seq[:]


		return 0

    def general_work(self, input_items, output_items):

		in_stream = input_items[0]
		if(len(input_items[0]) < 400):
			return 0
		cert = []

		for i in range(0,len(self.replacements)):
			cod = blkfinal.replacement(self,self.replacements[i], in_stream,self.replacementsize[i][0])
			if(cod ==self.replacementsize[i][0]):
				self.codificador= self.replacementsize[i][1]
				self.tamanho = self.replacementsize[i][0]
				self.count = 100
			else:
				if(self.count>0):
					self.count = self.count - 1
				else:
					self.codificador="..."
					self.tamanho = 1
				
			
		self.consume(0,len(input_items[0]))

		return 0