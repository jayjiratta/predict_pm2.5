import requests
from pprint import pformat

station_id = ['100t' ,'60t' ,'33t' ,'34t' ,'o61' ,'87t' ,'105t' ,'77t' ,'28t' ,'29t' ,'31t' ,'74t' ,'o21' ,'o38' ,'71t']
param = "PM25,PM10,O3,CO,NO2,SO2,WS,TEMP,RH,WD"
data_type = "hr"
start_date = "2024-02-19"
end_date = "2024-02-20"
start_time = "00"
end_time = "23"
url = f"http://air4thai.com/forweb/getHistoryData.php?stationID={station_id}&param={param}&type={data_type}&sdate={start_date}&edate={end_date}&stime={start_time}&etime={end_time}"
response = requests.get(url)
response_json = response.json()
# print(pformat(response_json))

import pandas as pd

pd_from_dict = pd.DataFrame.from_dict(response_json["stations"][0]["data"])
print(pformat(pd_from_dict))
pd_from_dict.to_csv(f"air4thai_{station_id}_{start_date}_{end_date}.csv")