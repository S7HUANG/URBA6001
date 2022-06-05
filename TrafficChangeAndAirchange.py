# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 16:24:49 2021

"""
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import pyproj
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mgwr.gwr import GWR

# pLot the map
def drawtrafficchangeandairchange(airpollution):    
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
    london1['change'] =(london1['2020']-london1['2015-19'])/london1['2015-19']
    fig, ax = plt.subplots(1,1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    ax=london1.plot(column = "change", k = 5, cmap ='Blues_r', legend = True,ax=ax, cax = cax, legend_kwds={'label':'Traffic flow between 2020 and 2015-19'})
    ax.set_xlim(-65000,45000)
    ax.set_ylim(6660000,6750000)
    NO2_location = pd.merge(NO2,all_location,on = 'Site')
    NO2_location['change'] = (NO2_location['2020'] -NO2_location['2015-19'])/ NO2_location['2015-19']
    points = gpd.GeoDataFrame(NO2_location,geometry = gpd.points_from_xy(NO2_location['@lng'],NO2_location['@lat'],crs = 'epsg:4326'))
    points = points.to_crs(epsg=3857)
    points_region = gpd.sjoin(points,london1)
    cax = divider.append_axes("right", size="5%", pad=0.75)
    points_region.plot(markersize = abs(points_region['change_left'])*80,column = 'change_left', cmap = 'OrRd',legend = True, cax =cax, legend_kwds={'anchor': (1.04, 0),'label':'Air change between 2020 and 2015-19'},ax=ax)
    plt.savefig(r'G:\6001python\picture\trafficandair_{}.png'.format(airpollution[17:23]),dpi =300)
    plt.show()
    
airpollution = r'G:\6001python\ALL_PM2.5_cleanednew.csv'
drawtrafficchangeandairchange(airpollution)
airpollution = r'G:\6001python\ALL_PM10_cleanednew.csv'
drawtrafficchangeandairchange(airpollution)
airpollution = r'G:\6001python\ALL_O3_cleanednew.csv'
drawtrafficchangeandairchange(airpollution)
airpollution = r'G:\6001python\ALL_NO2_cleanednew.csv'
drawtrafficchangeandairchange(airpollution)