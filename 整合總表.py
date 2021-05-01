### 整合委託與成交檔 ###

import pandas as pd
import glob

# use your path of 成交檔（事先刪除夜盤資料）
path = "/Users/alex_chiang/Documents/Fin_tech/201909_期交所_期貨練習/"
file_1 = sorted(glob.glob(path + "委託檔" + "/*.txt"))
file_2 = sorted(glob.glob(path + "成交檔" + "/*.txt"))

data = pd.DataFrame()
for i,j in zip(file_1, file_2):

    df1 = pd.read_csv(i, delimiter = "\t", header=None)
    df2 = pd.read_csv(j, delimiter = "\t", header=None)

    # 整理委託資料
    df1 = df1[df1[1].str.contains('TXF') == True]
    df1.iloc[:,0] = pd.to_datetime(df1.iloc[:,0], format='%Y%m%d')
    df1.iloc[:,9] = pd.to_timedelta(df1.iloc[:,9])
    df1['Datetime'] = df1.iloc[:,0] + df1.iloc[:,9]
    df1 = df1.sort_values(by = ['Datetime'])
    
    df1 = df1.drop(columns = [0,9,10,11]) #刪除不必要的資料
    df1.rename(columns={1:"product_id", 2: "position",
                         3:"委託量", 4: "未成交量",
                         5:"委託價", 6: "order_type",
                         7:"order_condition", 8: "position_type",
                         12:"key"}, inplace = True)

    # 整理成交資料
    df2 = df2[df2[1].str.contains('TXF') == True]
    df2.iloc[:,0] = pd.to_datetime(df2.iloc[:,0], format='%Y%m%d')
    df2 = df2.sort_values(by = [0,1,2]) #簡單做一下排序
    df2 = df2.dropna(axis = 1) #刪除 NAN
    
    df2.iloc[:,7] = pd.to_timedelta(df2.iloc[:,7])
    df2['成交時間'] = df2.iloc[:,0] + df2.iloc[:,7]
    df2 = df2.sort_values(by = ['成交時間']) #處理時間格式
    
    df2 = df2.drop(columns = [0,14,15,16]) #刪除不必要的資料
    df2.rename(columns={1:"product_id", 10:"position", 
                         11:"成交價", 12:"成交量",
                         13:"position_type", 17: "order_type",
                         18:"key"}, inplace = True)
        
    # 合併檔案
    df = df1.merge(df2, on = ['key', 'position', 'product_id', 'order_type', 'position_type'], how='left')
    df.set_index('Datetime', inplace = True)
    data = pd.concat([data, df], axis=0, sort=False)


# 抓出近月台指期，單邊交易資料
# 9/18(含)前：TXFI9
# 9/19(含)後：TXFJ9

data = data[data['product_id'].str.contains('/') == False]

p1 = data.loc[:'2019-09-18'][data.loc[:'2019-09-18']['product_id'].str.contains('TXFI9') == True]
p2 = data.loc['2019-09-19':][data.loc['2019-09-19':]['product_id'].str.contains('TXFJ9') == True]
data_only = pd.concat([p1,p2], axis=0, sort=False)


# 存檔
address = "/Users/alex_chiang/Documents/Fin_tech/201909_期交所_期貨練習/"
data_only.to_csv(address + "委託成交合併檔.csv")
#%%

### 整合揭示檔、委託檔、成交檔 ###

import pandas as pd

path = "/Users/alex_chiang/Documents/Fin_tech/201909_期交所_期貨練習/"
df1 = pd.read_csv(path + "揭示檔.csv")
df1['Datetime'] = pd.to_datetime(df1['Datetime'])

df2 = pd.read_csv(path + "委託成交合併檔.csv")
df2['Datetime'] = pd.to_datetime(df2['Datetime'])

# Google: python combine two dataframe with timestamp
# https://pse.is/3dqzp9

# Google: python merge_asof remain each key on
# https://pse.is/3fa5f7

# Google: python merge_asof match every index
# https://pse.is/3c84rj

# TypeError: Function call with ambiguous argument types
# Solved: key need to covert to datetime
# https://pse.is/3flgut

df = pd.merge_asof(df2.rename(columns={'Datetime':'委託時間'}), 
                   df1.rename(columns={'Datetime':'揭示時間'}), 
                   left_on = '委託時間',
                   right_on = '揭示時間',
                   direction = 'backward',
                   by = 'product_id',
                   tolerance = pd.Timedelta('2hr'))


# 確認正確與否
df_test = df.loc[:, ['委託時間','揭示時間']]
df_test = df_test.iloc[1150000:1500000]


# 存檔
address = "/Users/alex_chiang/Documents/Fin_tech/201909_期交所_期貨練習/"
df.to_csv(address + "揭示委託成交合併檔.csv")
