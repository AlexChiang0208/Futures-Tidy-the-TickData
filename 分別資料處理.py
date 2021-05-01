### 整理成交資料 ###

%reset -f
import pandas as pd
import glob

# use your path of 成交檔（事先刪除夜盤資料）
path = "/Users/alex_chiang/Documents/Fin_tech/201909_期交所_期貨練習/成交檔/"
files = sorted(glob.glob(path + "/*.txt"))

# 合併很多個 txt 檔
data = pd.DataFrame()

for i in files:
    temp = pd.read_csv(i, delimiter = "\t", header=None)
    data = pd.concat([data, temp], axis=0, sort=False)

# 簡單整理一下
data = data[data[1].str.contains('TXF') == True]
data.iloc[:,0] = pd.to_datetime(data.iloc[:,0], format='%Y%m%d')
data = data.sort_values(by = [0,1,2]) #簡單做一下排序
data = data.dropna(axis = 1) #刪除 NAN

# 時間魔術秀
data.iloc[:,7] = pd.to_timedelta(data.iloc[:,7])
data['Datetime'] = data.iloc[:,0] + data.iloc[:,7]
data = data.sort_values(by = ['Datetime'])
data.set_index('Datetime', inplace = True)
data = data.drop(columns = [0, 15])

# 更改欄位名
data = data.drop(columns = [14,16]) #刪除不必要的資料
data.rename(columns={1:"product_id", 10:"position", 
                     11:"price", 12:"quantity",
                     13:"position_type", 17: "order_type",
                     18:"key"}, inplace = True)


# 抓出近月台指期，單邊交易資料
# 9/18(含)前：TXFI9
# 9/19(含)後：TXFJ9

data = data[data['product_id'].str.contains('/') == False]

p1 = data.loc[:'2019-09-18'][data.loc[:'2019-09-18']['product_id'].str.contains('TXFI9') == True]
p2 = data.loc['2019-09-19':][data.loc['2019-09-19':]['product_id'].str.contains('TXFJ9') == True]
data_only = pd.concat([p1,p2], axis=0, sort=False)

# 存檔
address = "/Users/alex_chiang/Documents/Fin_tech/201909_期交所_期貨練習/"
data_only.to_csv(address + "成交檔.csv")
#%%

### 整理委託資料 ###

%reset -f
import pandas as pd
import glob

# use your path of 委託檔（事先刪除夜盤資料）
path = "/Users/alex_chiang/Documents/Fin_tech/201909_期交所_期貨練習/委託檔/"
files = sorted(glob.glob(path + "/*.txt"))

# 合併很多個 txt 檔
data = pd.DataFrame()

for i in files:
    temp = pd.read_csv(i, delimiter = "\t", header=None)
    temp = temp[temp[1].str.contains('TXF') == True]
    temp = temp.drop(columns = [10,11])
    data = pd.concat([data, temp], axis=0, sort=False)

# 時間格式整理
data.iloc[:,0] = pd.to_datetime(data.iloc[:,0], format='%Y%m%d')
data.iloc[:,9] = pd.to_timedelta(data.iloc[:,9])
data['Datetime'] = data.iloc[:,0] + data.iloc[:,9]
data = data.sort_values(by = ['Datetime'])
data.set_index('Datetime', inplace = True)
data = data.drop(columns = [0, 9])

# 更改欄位名
data.rename(columns={1:"product_id", 2: "position",
                     3:"quantity", 4: "un_quantity",
                     5:"price", 6: "order_type",
                     7:"order_condition", 8: "position_type",
                     12:"key"}, inplace = True)


# 抓出近月台指期，單邊交易資料
# 9/18(含)前：TXFI9
# 9/19(含)後：TXFJ9

data = data[data['product_id'].str.contains('/') == False]

p1 = data.loc[:'2019-09-18'][data.loc[:'2019-09-18']['product_id'].str.contains('TXFI9') == True]
p2 = data.loc['2019-09-19':][data.loc['2019-09-19':]['product_id'].str.contains('TXFJ9') == True]
data_only = pd.concat([p1,p2], axis=0, sort=False)

# 存檔
address = "/Users/alex_chiang/Documents/Fin_tech/201909_期交所_期貨練習/"
data_only.to_csv(address + "委託檔.csv")
#%%

### 整理揭示資料 ###

%reset -f
import pandas as pd
import glob

# use your path of 揭示檔（事先刪除夜盤資料）
path = "/Users/alex_chiang/Documents/Fin_tech/201909_期交所_期貨練習/揭示檔/"
files = sorted(glob.glob(path + "/*"))

# 合併很多個 txt 檔
data = pd.DataFrame()

for i in files:
    temp = pd.read_csv(i, delimiter = "\t", header=None)
    temp = temp[temp[1].str.contains('TXF') == True]
    
    # 時間格式整理
    date = pd.to_datetime(temp.iloc[:,0], format='%Y%m%d')
    time = pd.to_datetime(temp.iloc[:,2], format='%H%M%S%f').dt.time
    time = time.map(lambda x: str(x))
    time = pd.to_timedelta(time)
    temp['Datetime'] = date + time
    temp = temp.sort_values(by = ['Datetime'])
    temp.set_index('Datetime', inplace = True)
    temp = temp.drop(columns = [0, 2])    
    data = pd.concat([data, temp], axis=0, sort=False)

# 更改欄位名
data.rename(columns={1:"product_id",
                     3:"1_buy_price", 4: "1_buy_quantity",
                     5:"2_buy_price", 6: "2_buy_quantity",
                     7:"3_buy_price", 8: "3_buy_quantity",
                     9:"4_buy_price", 10:"4_buy_quantity",
                     11:"5_buy_price", 12:"5_buy_quantity",
                     13:"1_sell_price", 14:"1_sell_quantity",
                     15:"2_sell_price", 16:"2_sell_quantity",
                     17:"3_sell_price", 18:"3_sell_quantity",
                     19:"4_sell_price", 20:"4_sell_quantity",
                     21:"5_sell_price", 22:"5_sell_quantity",
                     23:"first_order_buy_price", 24:"first_order_buy_quantity",
                     25:"first_order_sell_price", 26:"first_order_sell_quantity"
                     }, inplace = True)

# 抓出近月台指期，單邊交易資料
# 9/18(含)前：TXFI9
# 9/19(含)後：TXFJ9

data = data[data['product_id'].str.contains('/') == False]

p1 = data.loc[:'2019-09-18'][data.loc[:'2019-09-18']['product_id'].str.contains('TXFI9') == True]
p2 = data.loc['2019-09-19':][data.loc['2019-09-19':]['product_id'].str.contains('TXFJ9') == True]
data_only = pd.concat([p1,p2], axis=0, sort=False)

# 存檔
address = "/Users/alex_chiang/Documents/Fin_tech/201909_期交所_期貨練習/"
data_only.to_csv(address + "揭示檔.csv")
