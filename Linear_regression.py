# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 10:20:19 2021

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import math
df = pd.read_csv(r'G:\6001python\for_regression.csv',index_col='month1')
df.columns = ["NO2","O3","PM10","PM25","driving","transit"]
print(df)
x = df['driving']
y = df['PM10']

# fit a linear curve an estimate its y-values and their error.
a, b = np.polyfit(x, y, deg=1)
y_est = a * x + b
y_err = x.std() * np.sqrt(1/len(x) +
                          (x - x.mean())**2 / np.sum((x - x.mean())**2))

fig, ax = plt.subplots(dpi = 200)
ax.plot(x, y_est, '-')
# ax.fill_between(x, y_est - y_err, y_est + y_err, alpha=0.2)
ax.plot(x, y, 'o', color='orange')
ax.set_xlabel("Mobility")
# ax.set_ylabel("NO2(ug/m³)")
ax.set_ylabel("PM10(refenrence equivalent)")