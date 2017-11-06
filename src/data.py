import os
import pandas

#  Parse data
location = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__))
)

filePath = os.path.join(location, '../nyse/prices-split-adjusted.csv')
data = pandas.read_csv(filePath, index_col = 'date')
