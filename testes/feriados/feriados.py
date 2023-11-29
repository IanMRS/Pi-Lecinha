from datetime import date
import holidays
import calendar

def get_brazilian_holidays(month, year):
    brazilian_holidays = holidays.country_holidays("BR")
    holidays_list = []

    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        if date(year, month, day) in brazilian_holidays:
            holidays_list.append(day)

    return holidays_list

# Example usage:
month = 11  # November
year = 2023
result = get_brazilian_holidays(month, year)
print(f"Brazilian Holidays in {calendar.month_name[month]} {year}: {result}")