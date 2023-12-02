from datetime import datetime, timedelta

def format_date(selected_date):
    """
    Format a date into a string.

    Parameters:
    - selected_date: The date to be formatted.

    Returns:
    A formatted date string.
    """
    if isinstance(selected_date, str):
        return selected_date
    return datetime.strftime(selected_date, "%Y%m%d")

def unformat_date(selected_date):
    """
    Unformat a date string into a formatted string.

    Parameters:
    - selected_date: The date string to be unformatted.

    Returns:
    A formatted date string.
    """
    try:
        parsed_date = datetime.strptime(str(selected_date), "%Y%m%d")
    except:
        parsed_date = datetime.strptime(str(selected_date), "%d%m%Y")
    return parsed_date.strftime("%d/%m/%y")

def get_days_between_dates(start_date_str, end_date_str):
        """
        Get a list of days between two dates.

        Parameters:
        - start_date_str: The start date string.
        - end_date_str: The end date string.

        Returns:
        A list of day strings between the start and end dates.
        """
        start_date = datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.strptime(end_date_str, "%Y%m%d")
        delta = end_date - start_date
        days_in_between = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
        result = [day.strftime("%Y%m%d") for day in days_in_between]
        return result