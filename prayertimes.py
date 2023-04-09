import requests
import json

import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


timings = []


def formatted_print(item):
    for obj in item:
        date = obj["date"]["timestamp"]
        temp = [date, get_time(obj, "Fajr"), get_time(obj, "Dhuhr"),
                get_time(obj, "Asr"), get_time(obj, "Maghrib"), get_time(obj, "Isha")]
        # text = json.dumps(temp, sort_keys=True, indent=4)
        timings.append(temp)
        # print(temp)


def get_time(item, prayer):
    return item["timings"][prayer].split(" ")[0]


def get_prayer_data(year, month, address):
    response = requests.get(
        f"http://api.aladhan.com/v1/calendarByAddress/{year}/{month}?address={address}")
    if response.status_code == 200:
        print(f"sucessfully fetched the data for {year}/{month}")
        # print(response.json.)
        formatted_print(response.json()["data"])
    else:
        print(
            f"Hello person, there's a {response.status_code} error with your request")


for i in range(1, 13):

    get_prayer_data(2023, i, "1906 Nueces St, Austin, TX 78705")

# print(timings)
df = pd.DataFrame(timings, columns=[
                  'Date', 'Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'])
df['Date'] = pd.to_datetime(df['Date'], unit='s')


# temp = df.apply(
#     lambda x: x.replace(hour=11, minute=59))
# df["Fajr"] = df["Dhuhr"] = df["Dhuhr"].apply(
#     lambda x: x.replace(year=1967, month=6, day=25)).tolist()

# df["Asr"] = df["Asr"].apply(
#     lambda x: x.replace(year=1967, month=6, day=25)).tolist()

# df["Maghrib"] = df["Maghrib"].apply(
#     lambda x: x.replace(year=1967, month=6, day=25)).tolist()

# df["Isha"] = df["Isha"].apply(
#     lambda x: x.replace(year=1967, month=6, day=25)).tolist()

# ax = plt.subplot()
# ax.plot(df.index, y)
# ax.yaxis.set_major_locator(HourLocator())
# ax.yaxis.set_major_formatter(DateFormatter('%H:%M'))
# df.iloc[:, 1:] = pd.to_datetime(df.iloc[:, 1:], format='%H:%M').dt.time

df.set_index('Date', inplace=True)

print(df)

df.to_excel("prayertimes.xlsx")

# # Create the plot
# fig, ax = plt.subplots(figsize=(10, 6))
# df.plot(ax=ax)

# # Set the axis labels and title
# ax.set_xlabel('Date')
# ax.set_ylabel('Time')
# ax.set_title('Prayer Timings')
# ax.yaxis.set_major_locator(HourLocator())
# ax.yaxis.set_major_formatter(DateFormatter('%H:%M'))

# Show the plot
# plt.show()
