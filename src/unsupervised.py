import operator, os
import pandas as pd
import seaborn
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from scipy import stats

from data import data

location = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__))
)


# Replace company symbols with numbers
data = pd.get_dummies(data, columns = ['symbol'])

columns = ['open', 'close', 'low', 'high', 'volume']

# Standardise: i.e. make it mathematically convenient to compare stuff
dataStandardised = stats.zscore(data[columns])

model = KMeans().fit(dataStandardised)
labels = model.labels_

data['clusters'] = labels
columns.extend(['clusters'])

fig1 = seaborn.lmplot(
	'close',
	'volume',
	data = data,
	fit_reg = False,
	hue = 'clusters'
)
fig1.savefig(os.path.join(location, '../plots/clusterCloseVolume.png'))

fig2 = seaborn.lmplot(
	'close',
	'high',
	data = data,
	fit_reg = False,
	hue = 'clusters'
)
fig2.savefig(os.path.join(location, '../plots/clusterCloseHigh.png'))


fig3 = seaborn.lmplot(
	'low',
	'high',
	data = data,
	fit_reg = False,
	hue = 'clusters'
)
fig3.savefig(os.path.join(location, '../plots/clusterLowHigh.png'))


plt.show()


