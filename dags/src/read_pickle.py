import pickle
import pandas as pd

data_from_pkl =[]
with open('/Users/venkysundar/Github/MLOps_Pipeline_Final/data/transformation/dateformat.pkl', 'rb') as f:
   
    object = pickle.load(f)
    df = pd.DataFrame(object)
    df.to_csv(r'pkl_data_data_format.csv')
