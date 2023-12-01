from datetime import datetime

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
    parsed_date = datetime.strptime(str(selected_date), "%Y%m%d")
    return parsed_date.strftime("%d/%m/%y")