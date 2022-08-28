import requests
import pandas as pd
import plotly.express as px

STOCKS = {
  "nvidia": "NVDA",
  "alphabet": "GOOGL",
  "microsoft": "MSFT",
  "meta-platform": "META",
  "apple": "AAPL"
}

def get_table(url, stock_name):
  html = requests.get(url).content
  df = pd.read_html(html)[0]
  df.columns = ['Date', 'Spending']
  df['Company'] = stock_name
  return df

def preprocess(df):
  df['Spending'] = df['Spending'].str.replace('$', '')
  df['Spending'] = df['Spending'].str.replace(',', '')
  df['Spending'] = pd.to_numeric(df['Spending'])
  return df

def save_data(stocks):
  df_spending = pd.DataFrame()
  for stock_name, ticker in stocks.items():
    url = f"https://www.macrotrends.net/stocks/charts/{ticker}/{stock_name}/research-development-expenses"
    df_spending = pd.concat([df_spending, get_table(url, stock_name)])

  df_spending = preprocess(df_spending)
  df_spending.to_csv('spending_data.csv')

  return df_spending

if __name__ == '__main__':
  save_data(STOCKS)

