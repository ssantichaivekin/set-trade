import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_daily_data(name_symbol) :
    '''
    Webscrape settrade website for information of name_symbol.
    This function will write a csv file containing the data scraped.
    It will also return a DataFrame of the data scraped. The DataFrame include:
        'date'          # The date of the row DD/MM/YY
        'start-val'     # The opening monetary value (baht)
        'max-val'       # max value (baht)
        'min-val'       # min value (baht)
        'avg-val'       # average value (baht)
        'close-val'     # closing value (baht)
        'monetary-diff' # difference between opening and closing value (baht)
        'precent-diff'  # % difference of monetary value
        'amount'        # amount traded that day (1000 unit)
        'value'         # value traded that day
        'set-index'     # set index
        'set-diff'      # change in set index from yesterday
    We will get the daily data of around 120 days before the current date.
    '''
    # This is the query website and the search parameter
    web = 'http://www.settrade.com/C04_02_stock_historical_p1.jsp'
    # Page 2 is the past daily data. Note that 'max' is capped to around 120
    # However, going over that number will not produce any error (but you will
    # get only around 120 rows of data).
    params = { 'txtSymbol': name_symbol, 'selectPage': 2, 'max': 200 }
    r = requests.get(web, params)
    # We create a BeautifulSoup object containing the request result
    soup = BeautifulSoup(r.text, 'lxml')

    data = []

    # Daily ata is in a table
    for row in soup.find_all('tr') :
        data_row = []
        # For all column in that row, add it to the data_row.
        for col in row.find_all('td') :
            # print(col.text, end=' ')
            data_row += [col.text]
        # Because we will get many wrong tables/rows, it is
        # necessary to filter the data. The best way I have found
        # is to check whether the row is of length 12. This is because
        # the information we want always have 12 fields.
        if len(data_row) == 12 :
            data += [data_row]
        # print()
        
    # Define the columns of the data
    columns = [
        'date',         # The date of the row DD/MM/YY
        'start-val',    # The opening monetary value (baht)
        'max-val',      # max value (baht)
        'min-val',      # min value (baht)
        'avg-val',      # average value (baht)
        'close-val',    # closing value (baht)
        'monetary-diff',# difference between opening and closing value (baht)
        'precent-diff', # % difference of monetary value
        'amount',       # amount traded that day (1000 unit)
        'value',        # value traded that day
        'set-index',    # set index
        'set-diff'      # change in set index from yesterday
        ]
    # create the DataFrame from 2-dimensional list
    df = pd.DataFrame(data, columns = columns)
    # write to file in the format: '(symbol)-webscraping-(date)'
    df.to_csv('%s-webscraping-%s.csv' % (name_symbol, df.date[0].replace('/', '-')))
    return df

# Driver function:
#  Test -- webscraping for BANPU info
if __name__ == '__main__' :
    scrape_daily_data('BANPU')