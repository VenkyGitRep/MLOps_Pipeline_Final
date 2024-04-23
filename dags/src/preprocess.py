import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

# Define the base directory
f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def preprocess():
    """
    Function to preprocess the raw data.
    
    Returns:
        pd.DataFrame: Preprocessed dataframe.
    """
    # Read the raw data
    data = pd.read_csv(os.path.join(f_dir, 'data', 'Online_Retail.csv'))
    
    # Remove rows with missing Description values
    data = data.dropna(subset=['Description'])
    
    # Drop unnecessary columns
    data = data.drop(columns=['Invoice', 'Description', 'Customer ID'], axis=1)
    
    # Filter out frequent StockCodes
    stock_code_counts = data['StockCode'].value_counts()
    frequent_stocks = stock_code_counts[(stock_code_counts >= 100) & (stock_code_counts <= 1000)].index.tolist()
    data_1 = data[data['StockCode'].isin(frequent_stocks)]

    # Extract date features
    data_1['InvoiceDate'] = pd.to_datetime(data_1['InvoiceDate'])
    data_1['Year'] = data_1['InvoiceDate'].dt.year
    data_1['Month'] = data_1['InvoiceDate'].dt.month
    data_1['Day'] = data_1['InvoiceDate'].dt.day
    data_1['Weekday'] = data_1['InvoiceDate'].dt.weekday
    
    # Convert StockCode and Country to numerical labels using LabelEncoder
    le = LabelEncoder()
    data_1['StockCode'] = le.fit_transform(data_1['StockCode'])
    data_1['Country'] = le.fit_transform(data_1['Country'])
    
    # Drop InvoiceDate column and filter out outliers
    data_1 = data_1.drop(columns=['InvoiceDate'], axis=1)
    data_2 = data_1.loc[(data_1['Quantity'] > 0) & (data_1['Quantity'] < 4000)]
    
    return data_2

def write_preprocessed_data():
    """
    Function to write preprocessed data to a CSV file.
    """
    preprocess().to_csv(os.path.join(f_dir, 'data', 'output.csv'), index=False)

if __name__ == "__main__":
   write_preprocessed_data()
