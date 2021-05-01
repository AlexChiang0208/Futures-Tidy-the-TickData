import pandas as pd

path = "/Users/alex_chiang/Documents/Fin_tech/201909_期交所_期貨練習/"
data = pd.read_csv(path + "成交檔.csv", parse_dates=True, index_col='Datetime')

### OHLCV ###
# 成交同時算入買入和賣出的資料，因此交易量會多兩倍

# 1分K
df_1min = data['price'].resample('1MIN').ohlc()
df_1min['volume_2times'] = data['quantity'].resample('1MIN').sum()
df_1min.dropna(inplace=True)
df_1min_talib = df_1min.rename(columns={'volume_2times':'volume'})
df_1min.rename(columns={'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'volume_2times':'Volume'}, inplace=True)

# 5分K
df_5min = data['price'].resample('5MIN').ohlc()
df_5min['volume_2times'] = data['quantity'].resample('5MIN').sum()
df_5min.dropna(inplace=True)
df_5min_talib = df_5min.rename(columns={'volume_2times':'volume'})
df_5min.rename(columns={'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'volume_2times':'Volume'}, inplace=True)

# 1時K
df_1hr = data['price'].resample('1H').ohlc()
df_1hr['volume_2times'] = data['quantity'].resample('1H').sum()
df_1hr.dropna(inplace=True)
df_1hr_talib = df_1hr.rename(columns={'volume_2times':'volume'})
df_1hr.rename(columns={'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'volume_2times':'Volume'}, inplace=True)

# 1天K
df_1day = data['price'].resample('1D').ohlc()
df_1day['volume_2times'] = data['quantity'].resample('1D').sum()
df_1day.dropna(inplace=True)
df_1day_talib = df_1day.rename(columns={'volume_2times':'volume'})
df_1day.rename(columns={'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'volume_2times':'Volume'}, inplace=True)
#%%

# mplfinance 靜態圖
# https://pse.is/3feb2z
# 官方文件：https://github.com/matplotlib/mplfinance

import mplfinance as mpf

# 基本款
mpf.plot(df_1day, type='candle', title = 'Futures - daily')
mpf.plot(df_1hr, type='line', title = 'Futures - hour')

# 增加均線
mpf.plot(df_1hr, type = 'candle', title = 'Futures - hour', mav = (5, 10, 20))
mpf.plot(df_1hr, type = 'line', title = 'Futures - hour', mav = (5, 10, 20))

# 增加指標、成交量、附加圖
## Talib（欄位名稱要用小寫；直接放 abstract 到 mpf 也可以，新增函式使閱讀更方便）
## VWAP https://pse.is/3ew2wa
from talib import abstract

def VWAP(df, window):
    price = (df['Close'] + df['High'] + df['Low'])/3
    VWAP = (price * df['Volume']).rolling(window).sum() / df['Volume'].rolling(window).sum()
    return VWAP

def EMA(df, period):
    return abstract.EMA(df, timeperiod=period)

def SMA(df, period):
    return abstract.SMA(df, timeperiod=period)

def RSI(df, period):
    return abstract.RSI(df, timeperiod=period)

index  = mpf.make_addplot(VWAP(df_1hr, 10), panel = 0, ylabel = 'VWAP')
mpf.plot(df_1hr, type = 'line', title = 'Futures - hour', addplot = [index])

index  = mpf.make_addplot(abstract.EMA(df_1hr_talib, 20), panel = 'lower', color = 'lime')
mpf.plot(df_1hr, type = 'line', title = 'Futures - hour', addplot = [index])

index  = mpf.make_addplot(SMA(df_1hr_talib, 20), panel = 1, ylabel = 'SMA 20')
mpf.plot(df_1hr, type = 'line', title = 'Futures - hour', addplot = [index])

index  = mpf.make_addplot(RSI(df_1hr_talib, 14), panel = 2, ylabel = 'RSI')
mpf.plot(df_1hr, type = 'line', title = 'Futures - hour', addplot = [index], volume = True)

# 改變風格
print(mpf.available_styles())
for i in mpf.available_styles():
    mpf.plot(df_1hr, type = 'candle', style = i, title = i, volume = True)

'''
在做的過程中，由於要將 panel = 'lower' 改成 panel = 1 的新版寫法，
更新了此套件，卻突然繪製不出來，報錯顯示：warn too much data。
嘗試過各種方法都無法解決，後來重新啟動 spyder，就可以恢復執行了！
2021/4/26 Version v0.12.7a17
'''
#%%

# plotly 動態圖（較為複雜，提供三種寫法）
# https://pse.is/3f6dsl
# 移除缺少時間：https://pse.is/3e4p7z
# 增加交易量圖：
# 官方文件：https://plotly.com/python

import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#1
ohlc = go.Candlestick(x = df_1min.index,
                       open = df_1min['Open'],
                       high = df_1min['High'],
                       low = df_1min['Low'],
                       close = df_1min['Close'])
data = [ohlc]
layout = dict(title = 'Future-1minute', 
              xaxis = dict(type = "category", categoryorder = 'category ascending'))
fig1 = go.Figure(data = data, layout = layout)
plotly.offline.plot(fig1, filename = path + 'Future_1minute.html', auto_open = False)


#2
fig2 = go.Figure(data = go.Ohlc(x = df_1hr.index,
                    open = df_1hr['Open'],
                    high = df_1hr['High'],
                    low = df_1hr['Low'],
                    close = df_1hr['Close']))
#fig2.layout = dict(title = 'Future-1hour', 
#                   xaxis = dict(type = "category", categoryorder = 'category ascending'))
plotly.offline.plot(fig2, filename = path + 'Future_1hour.html', auto_open = False)


#3
fig3 = go.Figure()
fig3.add_trace(go.Candlestick(x = df_1day.index,
                       open = df_1day['Open'],
                       high = df_1day['High'],
                       low = df_1day['Low'],
                       close = df_1day['Close']))
fig3.layout = dict(title = 'Future-1day',
                   xaxis = dict(type = "category", categoryorder = 'category ascending'))
plotly.offline.plot(fig3, filename = path + 'Future_1day.html', auto_open = False)
#%%

# cufflinks 動態圖（無敵簡單）
# 官方文件：https://github.com/santosjorge/cufflinks

import cufflinks as cf
import plotly


quant_fig = cf.QuantFig(df_1hr, title='Future - 1 hour', legend='top', name='Price')
quant_fig.add_bollinger_bands()
quant_fig.add_sma([10,20],width=2,color=['green','lightgreen'],legendgroup=True)
quant_fig.add_rsi(periods=20,color='java')
quant_fig.add_bollinger_bands(periods=20,boll_std=2,colors=['magenta','grey'],fill=True)
quant_fig.add_volume()
quant_fig.add_macd()

fig = go.Figure(data = quant_fig.iplot(asFigure=True))
#fig.layout = dict(xaxis = dict(type = "category"))
plotly.offline.plot(fig, filename = path + "Future_iplot.html", auto_open=False)


df.iplot()
# example
df=cf.datagen.ohlc()
qf=cf.QuantFig(df,title='First Quant Figure',legend='top',name='GS')
qf.add_bollinger_bands()
fig = go.Figure(data = qf.iplot(asFigure=True))
plotly.offline.plot(fig, filename = path + "Fut_iplot.html", auto_open=False)


# 我發現了啦！加了 dict(xaxis = dict(type = "category"))之後
# 雖然可以清除空值，但是會讓圖變得很奇怪（所以我的 plotly 成交量也才畫這麼不順）
# 解決方法應該是要去研究 layout 或是 go.Figure() 裡的參數



