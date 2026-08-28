import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 


def import_data():
    df = pd.read_csv("monitors.csv")
    return df

df = import_data()
print(df.head())



def check_data(df):
    print("\n Check for nulls:")
    print(df.isna().sum())



    return  df


check_data(df)


def data_analysis(df):
    summation = df.groupby(["brand"])["price"].sum()
    print("\n The Sum of prices by brand and condition is:")
    print(summation)

    return summation
    


data_analysis(df)




