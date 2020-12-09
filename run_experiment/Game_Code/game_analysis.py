###Network Game Analysis###
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import os 

###Load data###

frames1 = []
frames2 = []
counter = 0

for x in range(1,3):
	os.chdir('/Users/adolf/Documents/NRT-Hyperbolic_Search/game_data/part'+str(x)+'/hyperbolic')
	for filename in os.listdir(os.getcwd()):
		if filename.endswith(".csv"):
			#csvfiles.append(str(filename))
			frames1.append(pd.read_csv(filename))
hyperbolic = pd.concat(frames1)
#hyperbolic.drop([''], axis=1)
print(hyperbolic.head())
for x in range(1,3):
	os.chdir('/Users/adolf/Documents/NRT-Hyperbolic_Search/game_data/part'+str(x)+'/euclidean')
	for filename in os.listdir(os.getcwd()):
		if filename.endswith(".csv"):
			#csvfiles.append(str(filename))
			frames2.append(pd.read_csv(filename))
euclidean = pd.concat(frames2)
print(euclidean.head())
#score matrix, energy matrix, node matrix

##