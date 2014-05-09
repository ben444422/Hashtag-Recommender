#################
# 
# Graph the error rates for the
#
# python parser.py < LDA_data.txt
#
#################

import sys
import matplotlib 
import pylab
import matplotlib.pyplot as plt


num_hashtags = []
error_rates = []
default_rates = []

for line in sys.stdin:
	tokens = [float(tok.strip()) for tok in line.split(",")]
	num = tokens[0]
	error = tokens[1]
	num_hashtags.append(num)
	default_rates.append(1 - (1/num))
	error_rates.append(error)


fig = plt.figure()
pl = fig.add_subplot(111)


handles = []


handles.append(pl.scatter(num_hashtags, error_rates, c="blue"))
handles.append(pl.scatter(num_hashtags, default_rates, c="red"))
pl.legend(handles, ["Error Rate for LDA", "Error Rate from Random Guessing"], loc=4)

pl.set_title("Error Rate vs. Number of Hashtags Used")
pl.set_ylabel("Error Rate")
pl.set_xlabel("Number of Hashtags Used")
plt.show()



