import os
import pandas
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

# def valuesByStep(array, step):
# 	return array[::step]
#
#
# for key in pricesDict:
# 	priceEvery90Days = pricesDict[key][::90]
# 	pyplot.boxplot(priceEvery90Days)
# 	pyplot.suptitle('{} Close Price every 90 days'.format(key))
#
#
# 	pyplot.xticks(arange(3, len(priceEvery90Days), 3))
# 	pyplot.show()


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



statNames = ['min', 'max', 'mean', 'variance', 'skew', 'kurt']

for name in statNames:
	for multiplier in monthMultipliers:
		for i in range(6):
			# Plot min and max
			if i == 1:
				pyplot.bar([statsDict[multiplier][2][i]])
	# TODO finish this
	# pyplot.xticks(monthMultipliers)
	# pyplot.bar(monthMultipliers, means)
	# pyplot.subtitle('Name')
	# pyplot.show()
