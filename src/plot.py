import operator
import os
import pandas
from itertools import chain
from pprint import pprint
from numpy import array, arange
from matplotlib import pyplot
from scipy import stats


#  Parse data
__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__))
)

filePath = os.path.join(__location__, '../nyse/prices-split-adjusted.csv')

data = pandas.read_csv(filePath, index_col = 'date')
data['date'] = data.index

pricesDict = dict(data.groupby('symbol')['close'].apply(tuple))

# How I got the formula:
# https://imgur.com/gallery/MN3z7
def getAverageChange(symbol = '', step = 30, prices = pricesDict):
	stepped = prices[symbol][::step]
	length = len(stepped)

	if length > 1:
		return (stepped[-1] - stepped[0]) / (length - 1)

	return stepped[-1] - stepped[0]


# Get steps in days
monthMultipliers = [1, 2, 4, 6, 12, 24, 48]
steps = [number * 30 for number in monthMultipliers]


averageChanges = {}
for multiplier in monthMultipliers:
	averageChanges[multiplier] = []


for key in pricesDict:
	for index, step in enumerate(steps):
		averageChanges[monthMultipliers[index]].append(getAverageChange(key, step))

statsDict = {}
for multiplier in monthMultipliers:
	# n, minMax(tuple), mean, var, skew, kurt

	statsDict[multiplier] = tuple(stats.describe(averageChanges[multiplier]))
	# print(stats.describe(averageChanges[multiplier]))


statNames = ['n', 'min', 'max', 'mean', 'variance', 'skew', 'kurt']
# stats.describe returns tuple:

#
for name in statNames:
	if name == 'mean':
		means = []

		for multiplier in monthMultipliers:
			means.append(statsDict[multiplier][2])

		pyplot.bar(monthMultipliers, means)
		pyplot.title('{} segmentation price changes of S&P'.format(name))
		pyplot.xlabel('Segment Length (Months)')
		pyplot.ylabel(name)
		pyplot.xticks(monthMultipliers)
pyplot.show()
