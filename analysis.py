import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, ifft
import pandas as pd
from sklearn.preprocessing import normalize

df = pd.read_csv("data/wfp_food_prices_nga.csv")
df = df[["usdprice", "date"]]
df = df.drop(0)
df["usdprice"] = df["usdprice"].apply(pd.to_numeric)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(by='date')
df= df.groupby(by="date").mean()

# df["usdprice"] = (
#     df["usdprice"] - df["usdprice"].mean()
#     )/df["usdprice"].std()

# sampling rate
sr = 12
# sampling interval
ts = 1.0/sr
t = np.arange(0,1,ts)

X = fft(df["usdprice"])
N = len(X)
n = np.arange(N)
T = N/sr
freq = n/T 

# Throwing a time series thingo in...

X = fft(df["usdprice"])
N = len(X)
n = np.arange(N)
T = N/sr
freq = n/T 

plt.figure(figsize = (12, 6))
plt.subplot(121)

plt.stem(freq, np.abs(X), 'b', \
         markerfmt=" ", basefmt="-b")
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.xlim(0, 10)

plt.subplot(122)
plt.plot(df.index, ifft(X), 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()
