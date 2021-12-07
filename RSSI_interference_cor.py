from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
import pandas as pd

class TimeSeries:
    def __init__(self, name, csv_name, timecol_name, time_scale, resample_time_scale, interpolate_method):
        self.name = name
        self.df = read_csv(csv_name)
        self.df[timecol_name] = pd.to_datetime(self.df[timecol_name], unit=time_scale)
        self.ts = self.df.set_index(timecol_name)
        self.ts_upsampled= self.ts.resample(resample_time_scale).interpolate(method=interpolate_method)
        self.index = self.ts_upsampled.index

    def print(self, length):
        print(self.ts_upsampled.head(length))

    def plot(self, start, end):
        self.ts_upsampled[start:end].plot()
        pyplot.show()

RSSI = TimeSeries("RSSI", "June RSSI timestamp.csv", "Time", "ms", "S", "linear")
#RSSI.print(20)
#RSSI.plot(0,20)
TX = TimeSeries("TX", "June TX timestamp.csv", "Time", "ms", "S", "linear")
#TX.print(20)
#TX.plot(0,len(TX.ts_upsampled))
#RSSI.ts_upsampled = RSSI.ts_upsampled.drop(RSSI.index[0:5])

df = RSSI.ts_upsampled.join(TX.ts_upsampled, on='Time', lsuffix='_RSSI', rsuffix='_TX')
print(df.head(10))

# extract data
# 1min before TX drops to 0
# reset index to 0-N
df = df.reset_index()
#print(df.head(10))

index_list = []
look_back_count = 60 # 1 min
index = 0
end = len(df)
threshold = 10

while index < end:
    # find zero TX
    while index < end and df.loc[index, 'Val_TX'] >= threshold:
        index += 1

    if index != end:
        # append res
        index_list.append([i for i in range(max(0, index-look_back_count), min(index+1,end-1))])

    # find non-zero
    while index < end and df.loc[index, 'Val_TX'] <= threshold:
        index += 1

print(len(index_list))
for l in index_list:
    print(l, ',')
"""
for r in index_list:
    df.loc[r, ['Val_RSSI','Val_TX']].plot(secondary_y=['Val_TX'])
    pyplot.show()
"""


