from datetime import date
from services.emi_calculate import generate_due_dates

if __name__ == '__main__':
    start = date(2025, 12, 28)
    dates = generate_due_dates(start, 5, 'DAILY')
    for d in dates:
        print(d.isoformat())
