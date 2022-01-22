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

class LiveDataset(torch.utils.data.Dataset):
    def __init__(self, data, max_path=None, transform=None):
        self.data_path = data_path
        self.transform = transform
        self.mode = mode
        
        self.max_features = np.load(max_path)

        self.data = [data]
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        data = self.data[idx][1:].astype(np.float)
        data = data / self.max_features
        label = self.data[idx][0]
        
        if self.transform != None:
            data = self.transform(label)
        
        return data, label