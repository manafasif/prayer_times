import streamlit as st
import requests

from datetime import datetime
import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

from date_handler import *


current_date = dt.date.today()
one_year_later = current_date + dt.timedelta(days=365)


def formatted_print(item):
    data = []
    for obj in item:
        date = datetime.fromtimestamp(
            int(obj["date"]["timestamp"])).strftime("%Y-%m-%d %H:%M:%S")
        temp = [date, get_time(obj, "Fajr"), get_time(obj, "Dhuhr"), get_time(
            obj, "Asr"), get_time(obj, "Maghrib"), get_time(obj, "Isha")]
        data.append(temp)
    return data


def get_time(item, prayer):
    return item["timings"][prayer].split(" ")[0]


def get_prayer_data(year, month, address):
    response = requests.get(
        f"http://api.aladhan.com/v1/calendarByAddress/{year}/{month}?address={address}")
    if response.status_code == 200:
        return formatted_print(response.json()["data"])
    else:
        return []


def generate_prayer_times_graph(start_month, start_year, end_month, end_year, address):
    timings_data = []
    month_year_list = get_month_year_range(
        start_month, start_year, end_month, end_year)

    for month, year in month_year_list:
        timings_data.extend(get_prayer_data(year, month, address))

    if not timings_data:
        st.error("No data available.")
        return None

    df = pd.DataFrame(timings_data, columns=[
                      "Date", "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"])
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")

    for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
        df[f"{prayer}"] = pd.to_datetime(df[f"{prayer}"], format='%H:%M')
        df[f"{prayer}Minutes"] = df[f"{prayer}"].apply(
            lambda x: (x - datetime.combine(x.date(), datetime.min.time())).total_seconds() / 60)

    plt.figure(figsize=(10, 6))
    for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
        plt.plot(df["Date"], df[f"{prayer}Minutes"], label=prayer)

    plt.xlabel("Date")
    plt.ylabel("Time")
    y_ticks = range(0, int(df["IshaMinutes"].max()) + 60, 60)
    plt.yticks(y_ticks, [
               f"{int(minutes/60):02d}:{int(minutes%60):02d}" for minutes in y_ticks])
    plt.title("Prayer Timings")
    plt.legend()
    plt.grid()
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return buffer


# Streamlit UI
st.title("Prayer Times Visualization")
st.write("Generate graphs showing prayer times throughout the year with customizable options.")

# Input form for date range and address
with st.form("input_form"):
    # Date and Address Inputs
    start_date = st.date_input("Start Date", value=current_date)
    end_date = st.date_input("End Date", value=one_year_later)
    address = st.text_input("Address", value="Lombard, IL")

    # Customization Inputs
    graph_title = st.text_input("Graph Title", value="Prayer Timings")
    x_label = st.text_input("X-Axis Label", value="Date")
    y_label = st.text_input("Y-Axis Label", value="Time (minutes)")
    grid_lines = st.checkbox("Show Grid Lines", value=True)
    line_style = st.selectbox("Line Style", ["-", "--", "-.", ":"])
    color_palette = st.selectbox(
        "Color Palette", ["Default", "coolwarm", "viridis", "plasma", "cividis"])
    submitted = st.form_submit_button("Generate Graph")

# Function to generate month-year ranges based on date inputs


def get_month_year_range_from_dates(start_date, end_date):
    start_month = start_date.month
    start_year = start_date.year
    end_month = end_date.month
    end_year = end_date.year
    return get_month_year_range(start_month, start_year, end_month, end_year)

# Function to apply color palette


def apply_color_palette(palette, prayers):
    if palette == "Default":
        return {}
    colors = plt.cm.get_cmap(palette, len(prayers))
    return {prayer: colors(i) for i, prayer in enumerate(prayers)}


# Generate graph
if submitted:
    with st.spinner("Generating graph..."):
        timings_data = []
        month_year_list = get_month_year_range_from_dates(start_date, end_date)

        for month, year in month_year_list:
            timings_data.extend(get_prayer_data(year, month, address))

        if not timings_data:
            st.error("No data available.")
        else:
            df = pd.DataFrame(timings_data, columns=[
                              "Date", "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"])
            df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")

            for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
                df[f"{prayer}"] = pd.to_datetime(
                    df[f"{prayer}"], format='%H:%M')
                df[f"{prayer}Minutes"] = df[f"{prayer}"].apply(
                    lambda x: (x - datetime.combine(x.date(), datetime.min.time())).total_seconds() / 60)

            # Apply color palette
            colors = apply_color_palette(
                color_palette, ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"])

            plt.figure(figsize=(10, 6))
            for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
                plt.plot(df["Date"], df[f"{prayer}Minutes"], label=prayer,
                         linestyle=line_style, color=colors.get(prayer))

            plt.title(graph_title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)

            if grid_lines:
                plt.grid()

            y_ticks = range(0, int(df["IshaMinutes"].max()) + 60, 60)
            plt.yticks(y_ticks, [
                       f"{int(minutes/60):02d}:{int(minutes%60):02d}" for minutes in y_ticks])

            plt.legend()
            buffer = BytesIO()
            plt.savefig(buffer, format="png")
            buffer.seek(0)
            st.image(buffer, caption="Prayer Times Graph",
                     use_container_width=True)
