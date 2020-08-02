import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error as mse

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

def train_test_split(df, train_start, test_start):
    """This function splits the dataframe into training and testing sets
    parameters:
    df = dataframe that needs to be split
    train_start: the start time for training data with which to index the frame
    test_start: the end time for trainng data and start time for testing data
    return:
    train and test dataframes
    """
    
    train = df[train_start:test_start]
    test = df[test_start:]

    return train, test

def top_zipcodes_chicago_metro():
    """This function returns the top 15 zipcodes 
    with highest historical ROI for 5 year period
    and 2 year period
    """
    
    df = load_df()

    #subset for chicago metro area
    chicago_df = df[(df['Metro'] == 'Chicago')]

    #calculate ROI for 5years and 2 years
    chicago_df['ROI_5yrs'] = ((chicago_df['2018-04'] - chicago_df['2013-04'])/chicago_df['2013-04'])*100
    chicago_df['ROI_2yrs'] = ((chicago_df['2018-04'] - chicago_df['2016-04'])/chicago_df['2016-04'])*100

    #identify zipcodes based on top ROI for 5 and 2 year time period
    top_15_ROI5 = chicago_df.sort_values('ROI_5yrs', ascending=False)[:15].RegionName
    top_15_ROI2 = chicago_df.sort_values('ROI_2yrs', ascending=False)[:15].RegionName
    
    return top_15_ROI5.values, top_15_ROI2.values


def zipcodes_top27():
    """This function return the zipcodes with the best
    historical ROI rates
    """
    #top 15 for both time periods
    roi5_regions, roi2_regions = top_zipcodes_chicago_metro()
    
    
    #removing duplicates in our list
    regions = []
    for region in roi5_regions:
        regions.append(region)
    for region in roi2_regions:
        if region not in regions:
            regions.append(region)
    
    return regions


def load_data_top_27():
    
    #load df
    df = load_df()
    
    #collect column names
    colnames = list(df.columns)
    #isolate time period columns alone
    colnames = colnames[7:]
    #replacing NaNs as 1 for now to accomadate further df manipulation
    for colname in colnames:
        df[colname].fillna(value=1, inplace=True)

    #transforming from wide to long
    melted_df = melt_data(df)
    
    regions = zipcodes_top27()
    
    chicago_top_27 = pd.DataFrame()
    chicago_top_27['time'] = pd.date_range(start='1996-04-01', end='2018-04-01', freq='MS')
    chicago_top_27.set_index('time', inplace=True)
    for region in regions:
        chicago_top_27[region] = melted_df[melted_df['RegionName'] == region].value.values
    
    data = chicago_top_27['2013':]
    
    # replacing 1s with Nans as before
    for i in data:
        data[i].replace(1., np.NaN, inplace = True)
    
    return data

def sarima_orders(ts):
    
    p = q = d = range(0, 2)
    pdq = list(itertools.product(p, d , q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    print('SARIMA parameters...')
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = SARIMAX(ts,order=param,seasonal_order=param_seasonal,
                              enforce_stationarity=False,enforce_invertibility=False)
                results = mod.fit()
                print('ARIMA{}x{} - AIC:{}'.format(param,param_seasonal,results.aic))
                
            except: 
                print('hello')
                continue
    
def sarima_grid_search():
    """This function returns a list of sarima orders
    corresponding to the best AIC scores calculated for
    models fit on the variuos combinations of the orders
    """
    
    sarimax_orders = []
    for i in range(len(regions)):
        results = {}
        import itertools
        p = q = d = range(0, 2)
        pdq = list(itertools.product(p, d , q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
        print('Orders and AIC Results...')
        #for i in pdq:
        #    for s in seasonal_pdq:
        #        print('SARIMAX: {} x {}'.format(i, s))
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    mod =SARIMAX(train.iloc[:, i],order=param,seasonal_order=param_seasonal,
                                 enforce_stationarity=False,enforce_invertibility=False)
                    result = mod.fit()
                    results[result.aic] = (param, param_seasonal)
                    print('ARIMA{}x{} - AIC:{}'.format(param,param_seasonal,result.aic))
                except: 
                    print('hello')
                    continue
        min_ = np.min([x for x in results.keys() if str(x) != 'nan'])
        sarimax_orders.append(results[min_])
    
    return sarimax_orders

def sarima_models_for_27_zipcodes():
    #sarima orders after running grid search
    sarima_orders = [((1, 1, 0), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 0, 12)),
     ((1, 1, 0), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 1), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 0), (1, 1, 0, 12)),
     ((1, 1, 0), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 0), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 0, 12)),
     ((1, 1, 0), (1, 1, 0, 12)),
     ((1, 1, 0), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 0, 12)),
     ((1, 1, 0), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 0, 12)),
     ((1, 1, 0), (1, 1, 0, 12)),
     ((1, 1, 0), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 0), (1, 1, 0, 12)),
     ((1, 1, 1), (1, 1, 0, 12)),
     ((1, 1, 0), (1, 1, 0, 12))]
    
    #training models based on optimal sarima orders
    regions = zipcodes_top27()
    
    data = load_data_top_27()
    
    train, test = train_test_split(data, '2013-01-01', '2017-10-01')
    
    sarima_test_predictions = []
    sarima_models = []
    for i in range(len(regions)):
        model = SARIMAX(train.iloc[:, i], order=sarima_orders[i][0],
                        seasonal_order=sarima_orders[i][1],
                        enforce_invertibility=False, enforce_stationarity=False).fit()
        test_preds = model.predict(start=test.iloc[:, i].index[0],
                                   end=test.iloc[:, i].index[-1], typ='levels')
        sarima_test_predictions.append(test_preds)
        sarima_models.append(model)
    
    sns.set(font_scale=1)
    sns.set_style('white')
    pd.plotting.register_matplotlib_converters()
    fig, ax = plt.subplots(9, 3, figsize=(20, 18))
    i = 0
    for row in range(9):
        for col in range(3):
            err = round(np.sqrt(mse(test.iloc[:, i], sarima_test_predictions[i])),0)
            test.iloc[:, i].plot(ax=ax[row][col], color='blue',
                                 label='Actual :' + str(regions[i]))
            sarima_test_predictions[i].plot(ax=ax[row][col], color='k',
                                            label='Preds, RMSE = ' + str(err))
            ax[row][col].legend(loc='upper left')
            i += 1
    
    return plt.show()


def sarima_models_top_18():
    new_sarima_orders= [((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 1), (0, 1, 1, 12)),
     ((1, 1, 1), (0, 1, 1, 12)),
     ((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 1), (0, 1, 1, 12)),
     ((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 1), (0, 1, 1, 12)),
     ((0, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 1), (0, 1, 1, 12)),
     ((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 1), (0, 1, 1, 12)),
     ((0, 1, 1), (0, 1, 1, 12)),
     ((1, 1, 1), (1, 1, 0, 12)),
     ((0, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 1), (1, 1, 1, 12)),
     ((1, 1, 1), (0, 1, 1, 12))]
    
    codes = [60804, 60085, 60110, 60104, 60505, 60651,
             60073, 60436, 60120, 60165, 60160, 60641,
             60432, 46327, 60633, 46324, 60099, 46394]
    
    data = load_data_top_27()
    
    forecasts = {}
    for i, code in enumerate(codes):
        model = SARIMAX(data.loc[:, code], order=new_sarima_orders[i][0],
                        seasonal_order=new_sarima_orders[i][1],
                        enforce_invertibility=False,
                        enforce_stationarity=False).fit()
        forecasts[code] = model.forecast(steps=12).values
        
    return forecasts   
    
{
 "cells": [],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 4
}
