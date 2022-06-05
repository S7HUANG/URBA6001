# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 20:58:40 2021

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

result3 = pd.read_csv(r'G:\6001python\result3.csv')
result5 = pd.read_csv(r'G:\6001python\result5.csv')
result3 = result3.drop(['Dec.1'],axis =1)
result5 = result5.drop(['Dec.1'],axis =1)
print(result3)
fig, ax = plt.subplots(figsize=(5,4),dpi =200)
mean3 = result3.mean()
mean5 = result5.mean()
result3 = result3.fillna(value = mean3)
result5 = result5.fillna(value = mean3)
print(result3)



boxplot = ax.boxplot(result3,widths=0.2,patch_artist=True,
                      medianprops={"color": "red", "linewidth": 1},
                      boxprops={"facecolor": "orange", "edgecolor": "red",
                          "linewidth": 0.5},
                      whiskerprops = {"color": "orange","linestyle":"--" ,"linewidth": 0.5},
                      capprops={"color": "orange", "linewidth": 0.5},
                      showfliers = False)
locs=ax.get_xticks()
lineplot = ax.plot(locs,result3.mean(),linewidth =0.4)
plt.xticks(np.arange(24),['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov'],rotation='vertical')