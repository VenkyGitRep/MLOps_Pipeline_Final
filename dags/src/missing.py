import os
import pickle

# Determine the absolute path of the project directory
f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))

fin_path = os.path.join(f_dir, 'data', 'transformation','raw_invoices.pkl')
fout_path = os.path.join(f_dir, 'data', 'transformation','missing.pkl')

def null_handler(input=fin_path, output=fout_path):
    """
    This function is to help us read the pickle file and deal with 
    the missing value existing in the dataset. In this case, we
    only deal with the attributes with string values and we will
    handle the null value from the attributes with numbers in later
    section
    Args:
        input: the pickle file path
        output: Where you want to put the pickle file
                            after eliminating the missing values
    return:
        output
    """
    
    df = None
    # check if the pickle file exists and load the file
    if os.path.exists(input):
        with open(input, "rb") as f:
            df = pickle.load(f)
    else:
        raise FileNotFoundError()
    
    # the customerID and description are the key att and remove the null values
    df.set_index('Unnamed: 0',inplace = True)
    df = df.dropna(subset=['Customer ID', 'Description'])
    #There are also some other columns with num values,
    #we want to handle these atts by replacing the null value with mean
    col_pos = ['Quantity','Price']
    df.fillna(df[col_pos].mean())
    # data quality checks after doing the manipulations
    if df.isna().sum().sum() != 0:
        missing_count = df.isna().sum().sum()
        raise ValueError(missing_count)
    with open(output, "wb") as f:
        pickle.dump(df, f) 
    #print out the data to see the structure
    with open(output, 'rb') as f:
        data = pickle.load(f)
        print(data)
    return output

if __name__ == "__main__":
    unzip_f = null_handler(fin_path, fout_path)
    

