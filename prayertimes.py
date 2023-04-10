# This Python program fetches prayer timings from api.aladhan based on location provided
# It generates a connected scatterplot graph of different prayer times
# The program helps the Muslim community find free time to schedule meetings without conflicts
# The graph provides a great advantage in managing time effectively
# The program takes care of daylight savings to ensure accurate timings
# Overall, this sophisticated program is an essential asset for any Muslim seeking to manage their schedule effectively

import csv
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

timings = []


def formatted_print(item):
    for obj in item:
        date = datetime.fromtimestamp(int(obj["date"]["timestamp"])).strftime("%Y-%m-%d %H:%M:%S")
        temp = [date, get_time(obj, "Fajr"), get_time(obj, "Dhuhr"), get_time(obj, "Asr"), get_time(obj, "Maghrib"), get_time(obj, "Isha")]
        timings.append(temp)
        print(temp)


def get_time(item, prayer):
    return item["timings"][prayer].split(" ")[0]


def get_prayer_data(year, month, address):
    response = requests.get(f"http://api.aladhan.com/v1/calendarByAddress/{year}/{month}?address={address}")
    if response.status_code == 200:
        print(f"successfully fetched the data for {year}/{month}")
        formatted_print(response.json()["data"])
    else:
        print(f"Hello person, there's a {response.status_code} error with your request")


for i in range(1, 13):
    get_prayer_data(2023, i, "1906 Nueces St, Austin, TX 78705")

# Writing data to a csv file
with open("prayer_timings.csv", mode="w") as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"])
    writer.writerows(timings)


with open('prayer_timings.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)

    # Append the new column names to the header
    header.extend(['FajrMinutes', 'DhuhrMinutes', 'AsrMinutes', 'MaghribMinutes', 'IshaMinutes'])

    # Opening a new csv file to write the converted minutes in seperate row
    with open('prayerMinutes.csv', 'w', newline='') as new_csvfile:
        csvwriter = csv.writer(new_csvfile)
        csvwriter.writerow(header)

        # Looping over each row in the original csv file that we made after fetching the Json data
        for row in csvreader:
            # Converting the times to minutes
            fajr_minutes = (datetime.strptime(row[1], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
            duhr_minutes = (datetime.strptime(row[2], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
            asr_minutes = (datetime.strptime(row[3], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
            maghrib_minutes = (datetime.strptime(row[4], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0
            isha_minutes = (datetime.strptime(row[5], '%H:%M') - datetime(1900, 1, 1)).total_seconds() / 60.0

            # Appending the new columns to the row
            row.extend([fajr_minutes, duhr_minutes, asr_minutes, maghrib_minutes, isha_minutes])

            # Writing the row to the new csv file
            csvwriter.writerow(row)

# reading the csv file and parse the date and times into a pandas dataframe
df = pd.read_csv('prayerMinutes.csv', parse_dates=['Date'],
                 date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S', errors='coerce'))


# converting minutes to timedata and add to date using pandas dataframe
df['Fajr'] = pd.to_datetime(df['Date'].dt.date) + pd.to_timedelta(df['FajrMinutes'], unit='m')
df['Dhuhr'] = pd.to_datetime(df['Date'].dt.date) + pd.to_timedelta(df['DhuhrMinutes'], unit='m')
df['Asr'] = pd.to_datetime(df['Date'].dt.date) + pd.to_timedelta(df['AsrMinutes'], unit='m')
df['Maghrib'] = pd.to_datetime(df['Date'].dt.date) + pd.to_timedelta(df['MaghribMinutes'], unit='m')
df['Isha'] = pd.to_datetime(df['Date'].dt.date) + pd.to_timedelta(df['IshaMinutes'], unit='m')


# plotting the data using matplotlib and showing it
plt.plot(df['Date'], df['FajrMinutes'], label='Fajr')
plt.plot(df['Date'], df['DhuhrMinutes'], label='Dhuhr')
plt.plot(df['Date'], df['AsrMinutes'], label='Asr')
plt.plot(df['Date'], df['MaghribMinutes'], label='Maghrib')
plt.plot(df['Date'], df['IshaMinutes'], label='Isha')
plt.legend()
plt.show()