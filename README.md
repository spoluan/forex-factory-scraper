# Forex Factory Calendar Scraper

A script to scrape the Forex Factory calendar for economic events and store the data in CSV files.

## Description

This script scrapes the Forex Factory calendar for economic events, including the date, time, currency, event, impact level, actual value, forecast, and previous value. The data is saved in CSV files for each year.

## Dependencies

- Python 3.x
- `beautifulsoup4`
- `pandas`
- `cloudscraper`

You can install the required packages using pip:

```bash
pip install beautifulsoup4 pandas cloudscraper
```


## Sample Output

The script saves the scraped data in CSV files named forex_factory_calendar_<year>.csv in the datasets directory. Each file contains the following columns: 

| Date       | Time   | Currency | Event              | Impact | Actual | Forecast | Previous | Combined DateTime     |
|------------|--------|----------|--------------------|--------|--------|----------|----------|-----------------------|
| 2012-01-01 | 00:00  | USD      | Nonfarm Payrolls   | High   | 120K   | 100K     | 90K      | 2012-01-01 00:00:00   |
| 2012-01-08 | 09:00  | EUR      | ECB Interest Rate  | Medium | 1.25%  | 1.50%    | 1.75%    | 2012-01-08 09:00:00   |
| 2012-01-15 | 14:30  | GBP      | Inflation Report   | High   |        | 1.75%    | 1.85%    | 2012-01-15 14:30:00   |
