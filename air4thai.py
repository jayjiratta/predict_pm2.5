import requests
from pprint import pformat
import pandas as pd

station_id = '93t'
param = "PM25,PM10,O3,CO,NO2,SO2,WS,TEMP,RH,WD"

data_type = "hr"
start_date = "2023-01-01"
end_date = "2024-03-01"
start_time = "00"
end_time = "23"

url = f"http://air4thai.com/forweb/getHistoryData.php?stationID={station_id}&param={param}&type={data_type}&sdate={start_date}&edate={end_date}&stime={start_time}&etime={end_time}"
response = requests.get(url)
response_json = response.json()

pd_from_dict = pd.DataFrame.from_dict(response_json["stations"][0]["data"])
print(pformat(pd_from_dict))
df = pd.DataFrame(pd_from_dict)
df1 = df[df.isnull().sum(axis=1) < 3]
cl_null = ['DATETIMEDATA','PM25', 'PM10', 'O3', 'CO', 'NO2', 'SO2', 'WS', 'TEMP', 'RH', 'WD']
df2 = df1[cl_null] = df1[cl_null].fillna(df1[cl_null].mean().round(2))

df2.loc[df2["TEMP"] == 0, "TEMP"] = df2["TEMP"].mean().round(2)
df2.to_csv('Trang_clean.csv', index=True)

df2[['Date', 'Time']] = df2['DATETIMEDATA'].str.split(' ', expand=True)
df3 = df2.drop('DATETIMEDATA', axis=1)
df3 = df2.groupby(['Date']).mean().round(2)
df3.to_csv('mean_value.csv', index=True)

train_df = df2.iloc[:1143, :]
test_df = df2.iloc[1143:, :]
train_df = train_df.drop(columns=['DATETIMEDATA','Date','Time'])
test_df = test_df.drop(columns=['DATETIMEDATA','Date','Time'])
train_df.to_csv('train.csv', index=False)
test_df.to_csv('test.csv', index=False)