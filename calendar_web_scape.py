# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 16:06:09 2024

@author: SEVENDI ELDRIGE RIFKI POLUAN
"""
 
from bs4 import BeautifulSoup # pip install beautifulsoup4
import pandas as pd
import cloudscraper # pip install cloudscraper 
import datetime 
import os
 
def generate_urls_for_year(year):
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    delta = datetime.timedelta(weeks=1)
    current_date = start_date

    urls = []
    while current_date <= end_date:
        week_start = current_date.strftime('%b%d.%Y').lower()  # Format to 'jul21.2024'
        url = f'https://www.forexfactory.com/calendar?week={week_start}'
        urls.append(url)
        current_date += delta

    return urls

def get_impact_level(impact_class):
    if "impact-yel" in ' ' . join(impact_class):
        return "Non-economic"
    if "impact-gra" in ' ' . join(impact_class):
        return "Low"
    elif "impact-ora" in ' ' . join(impact_class):
        return "Medium"
    elif "impact-red" in ' ' . join(impact_class):
        return "High"
    else:
        return "None"
    
def format_date(date_str, year):
    try:
        parsed_date = datetime.datetime.strptime(date_str, '%a %b %d').replace(year=year)
        formatted_date = parsed_date.strftime('%Y-%m-%d')
        return formatted_date
    except ValueError:
        return date_str
    
def scrape_forexfactory(url, year):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'calendar__table'})
    rows = table.find_all('tr', {'class': 'calendar__row'})

    data = []
    last_time = ''
    for row in rows:
        date_cell = row.find_previous('tr', {'class': 'calendar__row--day-breaker'})
        date = date_cell.text.strip() if date_cell else ''
        formatted_date = format_date(date, year)
        
        time = row.find('td', {'class': 'calendar__time'}).text.strip() if row.find('td', {'class': 'calendar__time'}) else ''
        if time:
            last_time = time
        else:
            time = last_time
        
        currency = row.find('td', {'class': 'calendar__currency'}).text.strip() if row.find('td', {'class': 'calendar__currency'}) else ''
        event = row.find('td', {'class': 'calendar__event'}).text.strip() if row.find('td', {'class': 'calendar__event'}) else ''
        
        impact_cell = row.find('td', {'class': 'calendar__impact'})
        impact = get_impact_level(impact_cell.find('span').get('class', [])) if impact_cell and impact_cell.find('span') else 'None'
        
        actual = row.find('td', {'class': 'calendar__actual'}).text.strip() if row.find('td', {'class': 'calendar__actual'}) else ''
        forecast = row.find('td', {'class': 'calendar__forecast'}).text.strip() if row.find('td', {'class': 'calendar__forecast'}) else ''
        previous = row.find('td', {'class': 'calendar__previous'}).text.strip() if row.find('td', {'class': 'calendar__previous'}) else ''
        
        if len(formatted_date.strip()) > 0 and len(time.strip()) > 0 and len(currency.strip()) > 0 and len(event.strip()) > 0 and len(impact.strip()) > 0:
            data.append([formatted_date, time, currency, event, impact, actual, forecast, previous])

    return data

def scrape_year(year):
    urls = generate_urls_for_year(year=year) 
    all_data = []
    for url in urls[:]:
        print(f"... retrieve {url}")
        weekly_data = scrape_forexfactory(url, year)
        all_data.extend(weekly_data)
    return all_data

def is_valid_time_format(time_str):
    try:
        datetime.datetime.strptime(time_str, "%I:%M%p")
        return True
    except ValueError:
        return False

def is_valid_date(date_str, date_format):
    try:
        datetime.datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False
    
def convert_time(date, time, year):
    for date_format in ["%Y-%m-%d", "%Y/%m/%d", "%a %b %d"]:
        try:
            if date_format == "%a %b %d":
                if is_valid_date(date + f" {year}", "%a %b %d %Y"): 
                    parsed_date = datetime.datetime.strptime(date + f" {year}", "%a %b %d %Y")
                else:
                    continue
            else:
                parsed_date = datetime.datetime.strptime(date, date_format)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Date format not recognized: {date}")
        
    if time.lower() == "all day" or time.lower().startswith("day") or not is_valid_time_format(time):
        return parsed_date.replace(hour=0, minute=0, second=0)
    else:
        parsed_time = datetime.datetime.strptime(time, "%I:%M%p")
        return parsed_date.replace(hour=parsed_time.hour, minute=parsed_time.minute, second=parsed_time.second)
    
year_start = 2012
year_end = 2024  
for year in range(year_start, year_end):
    print(f"Start scrawling data for {year}")
    data = scrape_year(year)
    df = pd.DataFrame(data, columns=['Date', 'Time', 'Currency', 'Event', 'Impact', 'Actual', 'Forecast', 'Previous'])
     
    # Apply the function to create a new column with combined datetime
    df['Combined DateTime'] = df.apply(lambda row: convert_time(row['Date'], row['Time'], year), axis=1)
    df['Combined DateTime'] = df['Combined DateTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    saved_path = os.path.join("datasets")
    if not os.path.exists(saved_path):
        os.makedirs(saved_path)
    
    df.to_csv(os.path.join(saved_path, f'forex_factory_calendar_{year}.csv'), index=False)
    
    print(f'Data for the year {year} has been saved to forex_factory_calendar_{year}.csv')