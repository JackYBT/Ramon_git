import numpy as np
import os, sys
import csv
import pandas as pd
import matplotlib.pyplot as plt
import time, copy
from importlib import reload

import torch
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torch import optim, nn

class TestModel():
	def __init__(self, model_path, max_path):
		self.model = torch.load(model_path)
		self.model.eval()
		self.max = np.load(max_path)

	def run_trial(self, data):
		return self.model(data / self.max)





