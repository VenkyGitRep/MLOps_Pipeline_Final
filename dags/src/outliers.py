import os
import pickle
import pandas as pd
from scipy import stats
import numpy as np


f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))

fin_path = os.path.join(f_dir, 'data', 'transformation','groupby.pkl')
fout_path = os.path.join(f_dir, 'data', 'transformation','outliers.pkl')

def outlier_handler(input = fin_path, output = fout_path, threshold = 1.5):
    """
    This function is for us to handle the outliers in the data.
    Basically they are the attributes with numbers like quantity. 

    Args:
        input (str): The default file path to fin_path.
        output (str): The default output file path to fout_path.
        threshold(float): The default value you use to define the threshold of outliers detection.
    """
    #We first need to check if the file exists in the path
    if os.path.exists(input):
        with open(input, "rb") as f:
            df = pickle.load(f)
    else:
        raise FileNotFoundError()
    
    # calculate IQR for column Height
    Q1 = df['Quantity'].quantile(0.25)
    Q3 = df['Quantity'].quantile(0.75)
    IQR = Q3 - Q1

    # identify outliers
    outliers = df[(df['Quantity'] < Q1 - threshold * IQR) | (df['Quantity'] > Q3 + threshold * IQR)]
    df = df.drop(outliers.index)
    
    with open(output, "wb") as f:
        pickle.dump(df, f) 
    #print out the data to see the structure
    with open(output, 'rb') as f:
        data = pickle.load(f)
        print(data)
    return output

# if __name__ == "__main__":
#     unzip_f = outlier_handler(fin_path, fout_path)
        