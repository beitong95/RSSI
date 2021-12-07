from pandas import read_csv
from pandas import datetime
from matplotlib import pyplot
import matplotlib.pyplot as plt
import pandas as pd
from index import index_list
from scipy import signal
import numpy as np

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

RSSI = TimeSeries("RSSI", "June RSSI timestamp.csv", "Time", "ms", "S", "quadratic")
TX = TimeSeries("TX", "June TX timestamp.csv", "Time", "ms", "S", "quadratic")

df = RSSI.ts_upsampled.join(TX.ts_upsampled, on='Time', lsuffix='_RSSI', rsuffix='_TX')
df = df.reset_index()

extra = 0
sum_corr = 0
n = len(index_list[0])
for r in index_list:
    
    # calculate cross cor
    array1_raw = df.loc[r[0]-extra:r[-1]+extra, 'Val_RSSI'].to_numpy()
    array1 = array1_raw/np.linalg.norm(array1_raw)
    array2_raw = df.loc[r[0]-extra:r[-1]+extra, 'Val_TX'].to_numpy()
    array2 = array2_raw/np.linalg.norm(array2_raw)
    corr = signal.correlate(array2, array1, mode='same')/ np.sqrt(signal.correlate(array1, array1, mode='same')[int(n/2)] * signal.correlate(array2, array2, mode='same')[int(n/2)])
#    corr = signal.correlate(array1, array1, mode='same')


    sum_corr += max(abs(corr))

    """
    fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, figsize=(4.8, 4.8))
    ax_orig.plot(array1_raw)
    ax_orig.set_title('RSSI')
    ax_orig.set_xlabel('Sample Number')
    ax_noise.plot(array2_raw)
    ax_noise.set_title('TX Rate')
    ax_noise.set_xlabel('Sample Number')
    ax_corr.plot(corr)
    ax_corr.set_title('Cross-correlated signal')
    ax_corr.set_xlabel('Lag')
    ax_orig.margins(0, 0.1)
    ax_noise.margins(0, 0.1)
    ax_corr.margins(0, 0.1)
    fig.tight_layout()
    plt.show()
    """
    """
    plotdf = pd.DataFrame(np.stack((array1, array2, corr), axis=-1), columns = ['RSSI', 'TX', 'Corr'])
    plotdf.plot(secondary_y=['RSSI'])
    pyplot.show()
    """
    """
    pd.Series(corr).plot()
    pyplot.show()

    # plot
    df.loc[r[0]-extra:r[-1]+extra, ['Val_RSSI','Val_TX']].plot(secondary_y=['Val_TX'])
    pyplot.show()
    """
print('avg:', sum_corr/len(index_list))

