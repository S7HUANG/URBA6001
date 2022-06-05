# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 04:09:12 2021

"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

result3 = pd.read_csv(r'G:\6001python\result3.csv')
result5 = pd.read_csv(r'G:\6001python\result5.csv')
result3 = result3.drop(['Dec.1'],axis =1)
result5 = result5.drop(['Dec.1'],axis =1)
print(result3)
mean3 = result3.mean()
mean5 = result5.mean()
driving = result3.fillna(value = mean3)
transit = result5.fillna(value = mean3)
driving = result3.mean()[:-1]
transit = result5.mean()[:-1]
print(driving)

path = r'G:\6001python\ALL_NO2.csv'


def airmonth(path):
    df = pd.read_csv(path)

    df.ReadingDateTime = pd.to_datetime(df.ReadingDateTime,format = ("%d/%m/%Y %H:%M"))
    # print(df)
    # Create 3 new columns
    df[['year','month','day']] = df.ReadingDateTime.apply(lambda x: pd.Series(x.strftime("%Y,%m,%d").split(",")))
    # print(df)
    df['month1'] =df['year'] + df['month']
    df1 = df
    
    aQ1 = df1['Value'].quantile(0.25)
    aQ3 = df1['Value'].quantile(0.75)
    aIQR = aQ3 - aQ1
    filter = (df1['Value'] >= aQ1 - 1.5 * aIQR) & (df1['Value'] <= aQ3 + 1.5 *aIQR)
    df1 = df1[filter]
    df2021 = df1.loc[df1['year'].isin(['2020','2021'])]   
    df2021 = df2021.groupby(['month1']).mean()
    return(df2021)

NO2 = airmonth(r'G:\6001python\ALL_NO2.csv')
O3 = airmonth(r'G:\6001python\ALL_O3.csv')
PM10 = airmonth(r'G:\6001python\ALL_PM10.csv')
PM25 = airmonth(r'G:\6001python\ALL_PM2.5.csv')
index1 = NO2.index
driving.index = index1
transit.index = index1
newdf = pd.concat([NO2,O3,PM10,PM25,driving,transit],axis = 1)
newdf.to_csv(r'G:\6001python\for_regression.csv')
newdfcorr = newdf.corr(method='spearman')
lables = ["NO2","O3","PM10","PM25","driving","transit"]
fig, ax = plt.subplots(dpi =200)
im, cbar = heatmap(newdfcorr, lables, lables, ax=ax,
                   cmap="coolwarm", cbarlabel="relationship between air pollution and mobility")
texts = annotate_heatmap(im)
fig.tight_layout()
plt.show()