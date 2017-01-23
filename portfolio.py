import sys
import datetime
import argparse
import pandas as pd
from pandas_datareader import DataReader
from math import floor
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
matplotlib.rcParams['figure.figsize'] = (15, 8)

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--capital', type=int, default=10000, help='Capital you want to invest')
    parser.add_argument('-t', '--tickers', nargs='+', help='tickers of stocks you want to invest in', required=True)
    parser.add_argument('-s', '--startdate', help='start date formatted yyyy-mm-dd', required=True)
    parser.add_argument('-e', '--enddate', help='end date formatted yyyy-mm-dd', required=True)
    return parser

def getData(tickers, start, end):
    d = {}
    start = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    dates = pd.date_range(start, end, freq='D')
    df = pd.DataFrame(index=dates, columns=tickers)
    for ticker in tickers:
        df[ticker] = DataReader(ticker, "yahoo", start, end)['Adj Close']
    df=df.dropna(axis=0)
    return df

def buildPortfolio(startdate, enddate, tickers, capital=100000):
    data = getData(tickers, startdate, enddate)
    value = []
    cap_per_ticker = capital/(len(tickers))
    d={}
    for ticker in tickers:
        d[ticker] = floor(cap_per_ticker/data[ticker][0])
    for index, row in data.iterrows():
        total =0
        for ticker in tickers:
            total += d[ticker] * row[ticker]
        value.append(round(total))
    data['Portfolio Value'] = value
    return data

def comparePortolio(p1, p2):
    p1 = p1['Portfolio Value']
    p2 = p2['Portfolio Value']
    df = pd.concat([p1, p2], axis=1)
    df.columns = ['YOURS', 'SPY']
    your_percent_change = round(((df['YOURS'][-1] - df['YOURS'][0])/df['YOURS'][0])*100, 3)
    spy_percent_change = round(((df['SPY'][-1] - df['SPY'][0])/df['SPY'][0])*100, 3)
    your_spy = round(((df['YOURS'][-1] - df['SPY'][-1])/(df['SPY'][-1]))*100, 3)
    print('----------------------------------------------------------------')
    print('Your portfolio performed', your_percent_change, '% compared to', spy_percent_change, '% with SPY')
    if (your_spy > 0): print('Your portfolio is', your_spy, '% better than SPY')
    else: print('SPY performed better than your portfolio by', abs(your_spy), '%')
    print('----------------------------------------------------------------')
    return df

def run(capital, startdate, enddate, tickers):
    X = comparePortolio(buildPortfolio(startdate, enddate, tickers, capital), buildPortfolio(startdate, enddate, ['SPY'], capital))
    X.plot(title='Your Portfolio vs SPY')
    plt.show()


if __name__ == "__main__":
    arg = createParser().parse_args()
    run(arg.capital, arg.startdate, arg.enddate, arg.tickers)
    sys.exit()
