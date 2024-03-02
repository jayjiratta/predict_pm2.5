import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv("Trang.csv")
df = pd.DataFrame(data)

df1 = df[df.isnull().sum(axis=1) < 3]
cl_null = ['PM25', 'PM10', 'O3', 'CO', 'NO2', 'SO2', 'WS', 'TEMP', 'RH', 'WD']
df2 = df1[cl_null] = df1[cl_null].fillna(df1[cl_null].mean().round(2))

df3 = df2.join(df[['DATETIMEDATA']].set_axis(df.index))
df3[['Date', 'Time']] = df3['DATETIMEDATA'].str.split(' ', expand=True)
df4=df3.drop('DATETIMEDATA', axis=1)

new_cols = ['Date','Time','PM25','PM10','O3','CO','NO2','SO2','WS','TEMP','RH','WD']
df5 = df4[new_cols]

df5.to_csv('Trang_clean.csv', index=False)

df5["Date"] = pd.to_datetime(df5["Date"], format="%Y-%m-%d")
df5.sort_values("Date", inplace=True)

#
data = pd.read_csv("Trang_clean.csv")
df6 = pd.DataFrame(data)
df7 = df6.groupby(['Date']).mean().round(2)
df7.to_csv('mean_value.csv', index=False)