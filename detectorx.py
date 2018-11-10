import numpy as np
from gnuradio import gr

class blkfinal(gr.basic_block):
    def __init__(self):  # only default arguments here
        gr.basic_block.__init__(
            self,
            name='Decoder',
            in_sig=[np.int8],
            out_sig=[np.int8]
        )
        self.buffer_ = []
        self.codificador = "Not Detected"
        self.seq = []
        self.replacements = []
        self.replacementsize = []
        self.packet = []
        self.replacements.append(([((0,0,0,0,0,0,0,1), 32), ((0,1,1), 0), ((0,0,1), 1)]))
        self.replacements.append(([((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), 32),((0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1), 1),((0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0), 0),((0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0), 2)]))
        self.replacementsize.append(28)
        self.replacementsize.append(9)

    def retorna_sequencia_detectada(self):
        return self.seq

    def retorna_codificador_detectado(self):
        return self.codificador
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
				buffer_.append(32)
				oo += 1
				ii += 1
		size_b = len(buffer_)
		flag = 0
		pos = 0
		seq = np.zeros((tam),dtype=np.int8)
		for i in range(0,size_b):
			if(buffer_[i] == 32 and flag == 0 ):
				flag = 1

			elif(buffer_[i]!= 32 and flag ==1):
				seq[pos] = buffer_[i]
				pos=pos+1
				if(pos==tam):
					flag=2

			elif(flag == 2 and buffer_[i]==32):
				self.seq = seq[:]
				return tam
			else:
				pos  = 0
				flag = 0
				seq  = np.zeros((tam),dtype=np.int8)


		return 0



    def general_work(self, input_items, output_items):

		in_stream = input_items[0]
		if(len(input_items[0]) < 200):
			return 0
		cert = []

		for i in range(0,len(self.replacements)):
			cod = blkfinal.replacement(self,self.replacements[i], in_stream,self.replacementsize[i])
			if(cod ==12):
				self.codificador= "HT12E"
			elif(cod ==28):
				self.codificador="HT6P20B"
			elif(cod==9):
				self.codificador="HT6026"
				
				

            #print(len(self.buffer_))

            # if(blkfinal.checker(self,self.packet,i)):
            #     print(blkfinal.retorna_sequencia_detectada(self))
            #     print(blkfinal.retorna_codificador_detectado(self))
            #     self.consume(0,len(input_items[0]))

            # else:
		self.consume(0,len(input_items[0]))

		return 0