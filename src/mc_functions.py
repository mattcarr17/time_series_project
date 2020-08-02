import pandas as pd
import numpy as np

def melt_data(df):
    ''' Melt dataframe

    This function takes in a dataframe in wide format
    and melt's it to convert it to long format. This long format, 
    is the standard dataframe structure to be used for 
    time series analysis.

    Args
        df: dataframe in wide format
    
    Return:
        melted: dataframe in long format

    '''
    melted = pd.melt(df, id_vars=['RegionName', 'City', 'State', 'Metro', 'CountyName', 'RegionID', 'SizeRank'], var_name='time')
    melted['time'] = pd.to_datetime(melted['time'], infer_datetime_format=True)
    melted = melted.dropna(subset=['value'])
    return melted

def train_test_split(df, region, train_start, train_end):
    ''' perform's train test split on subset of dataframe

    This function takes in a dataframe, and selected region.
    It then performs a train test split using the train_start
    and train_end as indices for these splits. Analysis required
    filtering earlier dates. Train start is the first index of training
    data, train_end is last index of training data and first
    index of testing data. Testing data goes until last index of dataframe.

    Args
        df: dataframe to be filtered
        region: zip code that is used to subset dataframe
        train_start: first index (date) of training data
        train_end: last index (date) of training data, first index of testing data

    Return:
        region_train: training data for selected region
        region_test: testing data for selected region
 
    '''
    region_df = df[df['RegionName'] == region]

    melted_region = melt_data(region_df)
    melted_region.set_index('time', inplace=True)
    melted_region = melted_region['value']

    region_train = melted_region[train_start:train_end]
    region_test = melted_region[train_end:]

    return region_train, region_test

def stationarity_check(ts):
    ''' checks time series for stationarity

    This function uses rolling mean and standard deviation
    as well as the dickey-fuller test to check whether or not a
    time series is stationary. Function will output a visual, showing
    original time series, rolling mean and rolling standard deviation
    to visually analyze for stationarity. Function will also output
    results of dickey-fuller test. P-value of less than .05 indicates
    time series is stationary.

    Args
        ts: time series to be checked

    Returns
        None
    
    '''

    # Calculate rolling statistics
    roll_mean = ts.rolling(window=8, center=False).mean()
    roll_std = ts.rolling(window=8, center=False).std()
    
    # Perform the Dickey Fuller test
    dftest = adfuller(ts) 
    
    # Plot rolling statistics:
    fig = plt.figure(figsize=(12,6))
    orig = plt.plot(ts, color='blue',label='Original')
    mean = plt.plot(roll_mean, color='red', label='Rolling Mean')
    std = plt.plot(roll_std, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    
    # Print Dickey-Fuller test results
    print('Results of Dickey-Fuller Test: \n')

    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', 
                                             '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
    
    return None