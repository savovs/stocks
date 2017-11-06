import os
import pandas, seaborn
from matplotlib import pyplot as plt
from scipy import stats
from collections import Iterable

from data import data

location = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__))
)

pricesDict = dict(data.groupby('symbol')['close'].apply(tuple))
volumesDict = dict(data.groupby('symbol')['volume'].apply(tuple))

steppedPriceAndVol = {}


# Get average price change for company by symbol
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
	steppedPriceAndVol[key] = {
		'prices': {},
		'volumes': {}
	}

	for index, step in enumerate(steps):
		steppedPriceAndVol[key]['prices'][monthMultipliers[index]] = pricesDict[key][::step]
		steppedPriceAndVol[key]['volumes'][monthMultipliers[index]] = volumesDict[key][::step]

		averageChanges[monthMultipliers[index]].append(getAverageChange(key, step))

# Flattens out irregular lists of lists
def flatten(iterable):
	result = []

	if isinstance(iterable, Iterable):
		for item in iterable:
			result.extend(flatten(item))
	else:
		result.append(iterable)

	return result

statsDict = {}
for multiplier in monthMultipliers:
	# [n, (min, max), mean, var, skew, kurt]
	nonFlatStats = tuple(stats.describe(averageChanges[multiplier]))

	# Flatten and pop to [min, max, mean, var, skew, kurt]
	statsDict[multiplier] = flatten(nonFlatStats[1:])

statNames = ['Min', 'Max', 'Mean', 'Variance', 'Skewness', 'Kurtosis']

for i, name in enumerate(statNames):
	buff = []

	for multiplier in monthMultipliers:
		buff.append(statsDict[multiplier][i])

	fig, ax = plt.subplots()
	seaborn.barplot(monthMultipliers, buff, ax = ax)

	ax.set_title('Average Price Change')
	ax.set_xlabel('Segmentation Length in Months')
	ax.set_ylabel(name)

	fig.savefig(os.path.join(location, '../plots/averageChanges{}.png'.format(name)))


fig, ax = plt.subplots()
fig.suptitle('Distribution of Average Price Change Per Segmentation')

for key in averageChanges:
	seaborn.kdeplot(averageChanges[key], ax = ax, label = key)
	ax.set_xlim([-20, 60])

fig.savefig(os.path.join(location, '../plots/averageChangesKde.png'))
plt.show()