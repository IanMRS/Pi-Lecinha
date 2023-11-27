from datetime import datetime, timedelta

def get_days_between_dates(start_date_str, end_date_str):
    # Convert input date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y%m%d")
    end_date = datetime.strptime(end_date_str, "%Y%m%d")

    # Calculate the number of days between the two dates
    delta = end_date - start_date

    # Generate a list of all days in between, including start and end dates
    days_in_between = [start_date + timedelta(days=i) for i in range(delta.days + 1)]

    # Format the result as strings in the YYYYMMDD format
    result = [day.strftime("%Y%m%d") for day in days_in_between]

    return result

# Example usage:
start_date = "20221115"
end_date = "20230105"
result = get_days_between_dates(start_date, end_date)
print(result)
