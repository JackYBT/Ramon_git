import numpy as np
from cortex import Cortex
from multiprocessing import Process,Queue,Pipe
from lights import Lights

import torch

class Subscribe():
	def __init__(self, user, model_path, max_path, debug=False):
		self.lights = Lights()
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
		while True:
			eeg_d, pow_d = parent_conn.recv()
			pred = self.process_data(eeg_d,pow_d)
			print(pred)
			if (pred > 0.7): self.lights.set_speed(self.lights.speed + 0.1)
			if (pred < 0.3): self.lights.set_speed(self.lights.speed - 0.1)


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
