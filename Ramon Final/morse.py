import numpy as np
from cortex import Cortex
from multiprocessing import Process,Queue,Pipe
import sys

import torch

class Subscribe():
	def __init__(self, user, model_path, max_path, debug=False):
		self.user = user
		self.c = Cortex(user, debug_mode=debug)
		self.c.do_prepare_steps()
		self.model = torch.load(model_path)
		self.model.eval()
		self.max = np.load(max_path)

	def establish_pipe(self, streams):
		parent_conn, child_conn = Pipe()
		p = Process(target=self.c.sub_request_mod, args=(child_conn,streams,))
		p.start()
		i = 0
		sofar = ''

		Morse = {"01":"A", "1000":"B", "1010":"C", "100":"D", "0":"E", "0010":"F",
				  "110":"G", "0000":"H", "00":"I", "0111":"J","101":"K","0100":"L",
				  "11":"M","10":"N", "111":"O", "0110":"P", "1101":"Q", "010":"R",
				  "000":"S", "1":"T", "001":"U","0001":"V","011":"W","1001":"X",
				  "1011":"Y", "1100":"Z"}

		final_output = ''

		while True:
			eeg_d, pow_d = parent_conn.recv()
			pred = self.process_data(eeg_d,pow_d)
			print(pred)
			if i == 5:
				i = 0
				word = str(np.round(pred))
				sofar += word[1:-2]
				print("This is so far", sofar)
				line = input()
				if line == 'm':
					#word = sofar[1:-2]
					#print(word, sofar)
					print(Morse[sofar])
					final_output += Morse[sofar]
					sofar = ""
				elif line == 'b':
					break
				else:
					continue

			i += 1


	def process_data(self, eeg, pow_d):
		raw_eeg = np.stack(eeg)
		min_f = np.min(raw_eeg, axis=0)
		max_f = np.max(raw_eeg, axis=0)
		avg_f = np.mean(raw_eeg, axis=0)
		var_f = np.var(raw_eeg, axis=0)
		med_f = np.median(raw_eeg, axis=0)
		rest = np.stack(pow_d)
		rest = np.mean(rest,axis=0)
		features = np.concatenate([min_f,max_f,avg_f,var_f,med_f,rest])
		input = torch.tensor((features / self.max),dtype=torch.float32)
		return self.model(input).detach().numpy()

	def subscribe_print(self, streams):
		self.c.sub_request(streams)


user = {'license': 'a718b5f2-3470-4a0c-9862-0420ff78434b',
					'client_id': 'r9P9TKzrQ0bSpbNhO9eRGbFsHDS8w6ug1bYXRF34', 
					'client_secret': 'FhoWv8IRoiMIfkZapaHsVUTGvoExbeCNBMoSwfEcSk9KaLehjc7RqYxcnBBwwveOsRyWY9OJsHdrL4I1OUEU3AmkWwgGJjKYYQfYrArceo6VXI328PwZMshOw24cEm6c',
					'debit': 100}

streams = ['eeg', 'pow']
model_path = "./model/final.pth"
max_path = "./data/max_vals.npy"

s = Subscribe(user, model_path, max_path, debug=False)
# s.subscribe_print(streams)
s.establish_pipe(streams)
