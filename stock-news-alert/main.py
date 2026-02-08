import requests
import pandas as pd
import os
import smtplib
from email.message import EmailMessage

# Flags
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
STOCK_MOVE_THRESHOLD = 0.03

#  ALPHAV API flags
ALPHAV_END_POINT = 'https://www.alphavantage.co/query'
ALPHAV_API_KEY = os.environ.get('ALPHAV_API_KEY')
ALPHA_PARAMS = {
    'function':'TIME_SERIES_DAILY',
    'symbol':STOCK,
    'outputsize': 'compact',
    'apikey':ALPHAV_API_KEY
}

# NEWS API flags
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
NEWS_END_POINT = 'https://newsapi.org/v2/everything?'
NEWS_PARAMS = {
    'q':COMPANY_NAME,
    'from':'2026-02-06',
    'sortBy':'popularity',
    'apiKey':NEWS_API_KEY
}

# Email details
email_sender = 'john.dooe993@gmail.com'
email_password = os.environ.get('JD_EMAIL_PASS') # No spaces
email_receiver = ['john.dooe993@gmail.com']
smtp_server = "smtp.gmail.com"
port = 587

def check_stock_move(dataframe, threshold):
    dataframe = dataframe.sort_values('Date', ascending=False)
    latest_change = dataframe['% change'].iloc[0]
    if latest_change > threshold:
        get_news()
        # send_email(data)

def get_news():
    news_response = requests.get(url=NEWS_END_POINT, params=NEWS_PARAMS)
    news_response.raise_for_status()
    data = news_response.json()
    top_3 = data['articles'][:3]
    send_email(top_3)

def send_email(content):
    for item in content:
        subject = item['title']
        content = item['description']
        final_content = content + '\n\n' + item['url']

        msg = EmailMessage()
        msg['Subject'] = f'>{STOCK_MOVE_THRESHOLD*100}% move in {STOCK} - ' + subject
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg.set_content(final_content)

        with smtplib.SMTP('smtp.gmail.com', port=port) as connection:
            connection.starttls()
            connection.login(user=email_sender, password=email_password)
            connection.send_message(msg=msg)
            print('Email sent successfully.')

#  Getting the daily close prices for the stock on the last 100 business days
response = requests.get(url=ALPHAV_END_POINT, params=ALPHA_PARAMS)
response.raise_for_status()
data = response.json()
# print(data)

# Put the data in a new dict with {key:value} formate where key=date and value=close_price
time_series_dict = data['Time Series (Daily)']
new_dict = {item:float(data['4. close']) for (item,data) in time_series_dict.items()}

# Creating a pandas data frame, adjusting date to datetime format & make it sortable
stock_df = pd.DataFrame(new_dict.items(), columns=['Date','Close price'])
stock_df['Date'] = pd.to_datetime(stock_df['Date'])
stock_df = stock_df.sort_values('Date', ascending=True)

# Computing % change
stock_df['% change'] = stock_df['Close price'].pct_change()

check_stock_move(stock_df, STOCK_MOVE_THRESHOLD)