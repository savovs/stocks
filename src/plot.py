import os
import pandas
from numpy import array
from matplotlib import pyplot
from datetime import datetime
from pprint import pprint

#  Parse data
__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__))
)

filePath = os.path.join(__location__, '../nyse/prices-split-adjusted.csv')
data = pandas.read_csv(filePath, index_col = 'date')


dictWithClose = dict(data.groupby('symbol')['close'].apply(tuple))



print(dictWithClose.keys())
appleEvery90Days = dictWithClose['AAPL'][::90]

pprint(appleEvery90Days)
print(appleEvery90Days[1])
print(appleEvery90Days[-1])


# List Symbols
# print(data[:, 0])

# Symbol name
# print(data[0][0])

# All data for first symbol, in this case 'A'
# print(data[0][1].loc[:, ['close']])


# Save plots for each company
# for i in range(3):
# 	data[i][1].loc[:, ['close']].plot()
# 	pyplot.suptitle('Stock: ' + data[i][0])
# 	pyplot.savefig('test' + str(i) + '.jpg')

# print(data.shape)

# print(dictWithClose.keys())





# data[0][1].loc[:, ['close']].plot()
# pyplot.suptitle('Stock: ' + data[0][0])
# pyplot.show()
