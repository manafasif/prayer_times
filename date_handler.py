from datetime import datetime, timedelta


def get_month_year_range(start_month, start_year, end_month, end_year):
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)
    month_year_list = []

    while start_date <= end_date:
        month_year_list.append((start_date.month, start_date.year))
        if start_date.month == 12:
            start_date = start_date.replace(year=start_date.year+1, month=1)
        else:
            start_date = start_date + timedelta(days=32)
            start_date = start_date.replace(day=1)

    return month_year_list
