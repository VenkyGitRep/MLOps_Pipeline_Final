import os
import pickle
import pandas as pd
# from datetime import datetime

# Determine the absolute path of the project directory
f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))

fin_path = os.path.join(f_dir, 'data', 'transformation','total_cost.pkl')
fout_path = os.path.join(f_dir, 'data', 'transformation','dateformat.pkl')

def date_format(input = fin_path,output = fout_path):
    if os.path.exists(input):
        with open(input, "rb") as f:
            df = pickle.load(f)
    else:
        raise FileNotFoundError()
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']).dt.strftime('%Y-%m-%d')
    
    with open(output,'wb') as f:
        pickle.dump(df,f)
    with open(output, 'rb') as f:
        data = pickle.load(f)
        print(data)
    return output

# if __name__ == "__main__":
#     unzip_f = date_format(fin_path, fout_path)