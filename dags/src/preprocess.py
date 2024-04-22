import pandas as pd
from sklearn.metrics import r2_score

from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os
import mlflow
from sklearn.preprocessing import LabelEncoder
f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
os.path.join(f_dir, 'data', 'Online_Retail.csv')
def preprocess():
    data = pd.read_csv("data/Online_Retail.csv")
    data = data.dropna(subset=['Description'])
    data = data.drop(columns=['Invoice','Description','Customer ID'],axis=1)
    stock_code_counts = data['StockCode'].value_counts()
    frequent_stocks = stock_code_counts[(stock_code_counts >= 100) & (stock_code_counts <= 1000)].index.tolist()
    data_1 = data[data['StockCode'].isin(frequent_stocks)]

    data_1['InvoiceDate'] = pd.to_datetime(data_1['InvoiceDate'])
    data_1['Year'] = data_1['InvoiceDate'].dt.year
    data_1['Month'] = data_1['InvoiceDate'].dt.month
    data_1['Day'] = data_1['InvoiceDate'].dt.day
    data_1['Weekday'] = data_1['InvoiceDate'].dt.weekday
    data_1['StockCode'] = data_1['StockCode'].astype(str)



    le = LabelEncoder()
    data_1['StockCode'] = le.fit_transform(data_1['StockCode'])
    data_1['Country']=le.fit_transform(data_1['Country'])
    le = LabelEncoder()
    data_1['StockCode'] = le.fit_transform(data_1['StockCode'])
    data_1['Country']=le.fit_transform(data_1['Country'])
    data_1 = data_1.drop(columns=['InvoiceDate'], axis=1)
    data_2 = data_1.loc[(data_1['Quantity']>0) & (data_1['Quantity']<4000)]
    

    
    return data_2


def write_preprocessed_data():
    preprocess().to_csv('data/output.csv', index=False)

'''

'''
if __name__ == "__main__":
   write_preprocessed_data()