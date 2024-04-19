import os
import pickle

# Determine the absolute path of the project directory
f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))

fin_path = os.path.join(f_dir, 'data', 'transformation','duplicates.pkl')
fout_path = os.path.join(f_dir, 'data', 'transformation','total_cost.pkl')

def total_cost(input = fin_path, output = fout_path):
    """This function is for us to create a new column called 
    total_cost which is the target value in this project.

    Args:
        input (str): the file path of input file which is the file after handle the duplicates
        output (str): the output file path which is the data set with a new column
    """
    #check if the data file exists in the path
    if os.path.exists(input):
        with open(input, "rb") as f:
            df = pickle.load(f)
    else:
        raise FileNotFoundError()
    
    df = df[df['Quantity']>0]
    df = df[df['Price']>0]
    df['total_cost'] = df['Quantity']*df['Price']
    
    with open(output,'wb') as f:
        pickle.dump(df,f)
    with open(output, 'rb') as f:
        data = pickle.load(f)
        print(data)
    return output

# if __name__ == "__main__":
#     unzip_f = total_cost(fin_path, fout_path)