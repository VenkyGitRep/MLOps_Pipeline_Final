import pandas as pd
import pickle
import os
import pandas as pd

f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
input_pickle_path = os.path.join(f_dir, 'data', 'transformation', 'raw_invoices.pkl')
data_path = os.path.join(f_dir, 'data', 'Online_Retail.csv')
# pd.read_excel(data_path)
def load_data(input=input_pickle_path, csv_path=data_path):
   print("Its all good")

if __name__ == "__main__":
    unzip_f = load_data(input_pickle_path, data_path)

