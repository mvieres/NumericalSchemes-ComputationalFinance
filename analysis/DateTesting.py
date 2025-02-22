from datetime import date, datetime


def date_to_float(input_date: str) -> float:
    # Define the reference date (Unix epoch)
    reference_date = datetime(1970, 1, 1)

    # Convert the input date string to a datetime object
    given_date = datetime.strptime(input_date, '%Y-%m-%d')

    # Calculate the difference in days
    delta = given_date - reference_date

    # Convert the difference to a float
    return delta.total_seconds() / (24 * 3600)


def convert_date(input_date: str) -> date:
    # Convert the input date string to a datetime object
    given_date = datetime.strptime(input_date, '%Y-%m-%d')

    # Extract the year, month, and day
    year = given_date.year
    month = given_date.month
    day = given_date.day

    # Return a date object
    return date(year, month, day)

today = date.today()
# Example usage
input_date = '2024-09-20'
date1 = convert_date(input_date)
print(date1.toordinal()-today.toordinal())