import pandas as pd
import numpy as np

def melt_data(df):
    melted = pd.melt(df, id_vars=['RegionName', 'City', 'State', 'Metro', 'CountyName', 'RegionID', 'SizeRank'], var_name='time')
    melted['time'] = pd.to_datetime(melted['time'], infer_datetime_format=True)
    melted = melted.dropna(subset=['value'])
    return melted

def train_test_split(df, region, train_start, train_end, test_start):
    region_df = df[df['RegionName'] == region]

    melted_region = melt_data(region_df)
    melted_region.set_index('time', inplace=True)
    melted_region = melted_region['value']

    region_train = melted_region[train_start:train_end]
    region_test = melted_region[test_start:]

    return region_train, region_test