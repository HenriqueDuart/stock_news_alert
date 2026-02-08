import requests
import pandas as pd
import os

# Flags
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_MOVE_THRESHOLD = 0.05



#  API flags
END_POINT = 'https://www.alphavantage.co/query'
ALPHAV_API_KEY = os.environ.get('ALPHAV_API_KEY')
ALPHA_PARAMS = {
    'function':'TIME_SERIES_DAILY',
    'symbol':STOCK,
    'outputsize': 'compact',
    'apikey':ALPHAV_API_KEY
}

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#  Getting the daily close prices for the stock on the last 100 business days
response = requests.get(url=END_POINT, params=ALPHA_PARAMS)
response.raise_for_status()
data = response.json()

# Put the data in a new dict with {key:value} formate where key=date and value=close_price
time_series_dict = data['Time Series (Daily)']
new_dict = {item:float(data['4. close']) for (item,data) in time_series_dict.items()}

# Creating a pandas data frame, adjusting date to datetime format & make it sortable
stock_df = pd.DataFrame(new_dict.items(), columns=['Date','Close price'])
stock_df['Date'] = pd.to_datetime(stock_df['Date'])
stock_df = stock_df.sort_values('Date', ascending=True)

# Computing % change
stock_df['% change'] = stock_df['Close price'].pct_change()
stock_df = stock_df.sort_values('Date', ascending=False)
print(stock_df.head(5))

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

