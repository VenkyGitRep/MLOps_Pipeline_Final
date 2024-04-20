import os
import pickle

# Determine the absolute path of the project directory
f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))

fin_path = os.path.join(f_dir, 'data', 'transformation','dateformat.pkl')
fout_path = os.path.join(f_dir, 'data', 'transformation','groupby.pkl')

def groupby(input = fin_path, output = fout_path):
    """This function is for us to do the groupby function based on the date
    that we just formated

    Args:
        input (str): the data file from the dateformat.pkl
        output (str): the data file that would be output as groupby.pkl
    """
    if os.path.exists(input):
        with open(input, "rb") as f:
            df = pickle.load(f)
    else:
        raise FileNotFoundError()
    
    df = df.groupby('InvoiceDate').agg({
        'Invoice':'nunique',
        'total_cost':'sum',
        'Quantity':'sum'
    }).reset_index()
    df = df.sort_values(by = 'InvoiceDate')
    
    with open(output, "wb") as f:
        pickle.dump(df, f) 
    #print out the data to see the structure
    with open(output, 'rb') as f:
        data = pickle.load(f)
        print(data)
    return output

if __name__ == "__main__":
    unzip_f = groupby(fin_path, fout_path)
    