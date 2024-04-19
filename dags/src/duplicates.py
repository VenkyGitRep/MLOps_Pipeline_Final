import os
import pickle

# Determine the absolute path of the project directory
f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))

fin_path = os.path.join(f_dir, 'data', 'transformation','missing.pkl')
fout_path = os.path.join(f_dir, 'data', 'transformation','duplicates.pkl')

def handle_duplicates(input = fin_path,output = fout_path):
    """
    This function is for us to detect the duplicates in the data and remove the duplicates data
    so that we can have a better data structure.
    Args:
        input (str): path for the input data file which is the data without missing values
        output (str): path for the output data which is the data without duplication
    """
    #Check if the path exists
    if os.path.exists(input):
        with open(input, "rb") as f:
            df = pickle.load(f)
    else:
        raise FileNotFoundError()
    
    df.drop_duplicates(inplace = True)
    with open(output, "wb") as f:
        pickle.dump(df, f) 
    #print out the data to see the structure
    with open(output, 'rb') as f:
        data = pickle.load(f)
        print(data)
    return output

# if __name__ == "__main__":
#     unzip_f = handle_duplicates(fin_path, fout_path)