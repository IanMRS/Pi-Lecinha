from datetime import datetime

def format_date(selected_date):
    if isinstance(selected_date, str):
        return selected_date
    return datetime.strftime(selected_date, "%Y%m%d")

def unformat_date(selected_date):
    parsed_date = datetime.strptime(str(selected_date), "%Y%m%d")
    return parsed_date.strftime("%d/%m/%y")