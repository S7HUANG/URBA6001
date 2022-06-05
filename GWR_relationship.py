# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 18:20:50 2021

"""

import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import pyproj
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mgwr.gwr import GWR


def gwrrelationship(airpollution):
    path = r'G:\6001python\LondonBoroughs.shp'
    NO2 = pd.read_csv(airpollution)
    all_location = pd.read_csv(r"G:\6001python\site\NO2sites.csv")
    all_location = all_location.rename(columns ={'@code' :'Site'})
    traffic = pd.read_csv(r'G:\6001python\traffic-flow-borough.csv',thousands=',')
    traffic = traffic.rename(columns ={'Local Authority' :'NAME'})
    london = gpd.read_file(path)
    london1 = pd.merge(london,traffic,on = 'NAME')
    london1['2020'] = london1['2020'].astype('float')
    london1['2015-19'] = (london1['2015'] + london1['2016']+ london1['2017']+ london1['2018']+ london1['2019']) / 5
    london1['change'] =london1['2020']/london1['2015-19']
    fig, ax = plt.subplots(1,1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)    
    ax=london1.plot(color = 'lightblue',edgecolor='white')
    ax.set_xlim(-65000,45000)
    ax.set_ylim(6660000,6750000)
    NO2_location = pd.merge(NO2,all_location,on = 'Site')
    NO2_location['change'] = NO2_location['2020'] / NO2_location['2015-19']
    points = gpd.GeoDataFrame(NO2_location,geometry = gpd.points_from_xy(NO2_location['@lng'],NO2_location['@lat'],crs = 'epsg:4326'))
    points = points.to_crs(epsg=3857)
    points_region = gpd.sjoin(points,london1)
    coords = points_region[['@lng','@lat']]
    coords = [tuple(x) for x in coords.values]
    y = np.array(points_region[['change_left']])
    x = np.array(points_region[['change_right']])
    x = (x - x.mean(axis=0)) / x.std(axis=0)
    y = (y - y.mean(axis=0)) / y.std(axis=0)
    model = GWR(coords, y, x, bw=10.000, fixed=False, constant =False, kernel='bisquare',spherical = True)
    results = model.fit()
    points_region['coefficient'] = results.params
    results.summary()
    points_region.plot(markersize=abs(points_region['coefficient'])*30,column='coefficient',cmap = 'OrRd',legend = True, ax=ax)
    plt.savefig(r'G:\6001python\picture\gwr_{}.png'.format(airpollution[17:23]),dpi =300)
    plt.show()
airpollution = r'G:\6001python\ALL_PM2.5_cleaned.csv'
gwrrelationship(airpollution)
airpollution = r'G:\6001python\ALL_PM10_cleaned.csv'
gwrrelationship(airpollution)
airpollution = r'G:\6001python\ALL_O3_cleaned.csv'
gwrrelationship(airpollution)
airpollution = r'G:\6001python\ALL_NO2_cleaned.csv'
gwrrelationship(airpollution)