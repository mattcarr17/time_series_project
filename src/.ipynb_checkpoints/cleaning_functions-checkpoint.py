import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_datetimes(df):
    return pd.to_datetime(df.columns.values[1:], format='%Y-%m')


def melt_data(df):
    """This function converts the wide dataframe 
    into the long format
    
    Returns: the dataframe with datetime object and values
    for home saleprices for each region
    """
    
    melted = pd.melt(df, id_vars=['RegionName', 'City',
                                  'State', 'Metro', 'CountyName', 'RegionID', 'SizeRank'],
                     var_name='time')
    melted['time'] = pd.to_datetime(melted['time'], infer_datetime_format=True)
    melted = melted.dropna(subset=['value'])
    
    return melted


def load_df():
    """This function uses pandas to read the 
    csv file and convert it into a dataframe
    """
    df = pd.read_csv('../../data/zillow_data.csv')
    
    return df 

def chicago_df():
    """This function returns the dataframe with
    chicago metropolitan zipcodes and the median 
    home saleprices in the long format
    """
    #helper funstion to load csv as df
    #path = '../../data/zillow_data.csv'
    df = load_df()
    
    #shortlisting chicago metro area
    chicago_df = df[(df['Metro'] == 'Chicago') & (df['State'] == 'IL')]
    
    #caluculating ROI 5yrs & 2yrs
    chicago_df['ROI_5yrs'] = ((chicago_df['2018-04'] -chicago_df['2013-04'])/
                              chicago_df['2013-04'])*100
    chicago_df['ROI_2yrs'] = ((chicago_df['2018-04'] - chicago_df['2016-04'])/
                              chicago_df['2016-04'])*100
    
    #sorting dataframe based on calculated ROIs
    top_30 = chicago_df.sort_values(
        'ROI_5yrs', ascending=False)[:100].sort_values(
        'ROI_2yrs',ascending=False)[:30]
    
    #wide to long format
    melted = pd.melt(top_30, id_vars=['RegionName', 'City','State',
                                      'Metro', 'CountyName','RegionID',
                                      'SizeRank', 'ROI_5yrs', 'ROI_2yrs' ],
                     var_name='time')
    melted['time'] = pd.to_datetime(melted['time'], infer_datetime_format=True)
    melted = melted.dropna(subset=['value'])
    
    #top 30 zipcodes
    regions = melted.sort_values('ROI_2yrs', ascending=False).RegionName.unique()
    
    #setting up timeseries dataframe
    new_df = pd.DataFrame()
    new_df['time'] = pd.date_range(start='1996-04-01', end='2018-04-01', freq='MS')
    new_df.set_index('time', inplace=True)
    for region in regions:
        new_df[region] = melted[melted['RegionName'] == region].value.values
    
    return new_df, regions

{
 "cells": [],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 4
}
