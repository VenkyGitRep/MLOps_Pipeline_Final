import pandas as pd
import pickle
import os
import pandas as pd

f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
input_pickle_path = os.path.join(f_dir, 'data', 'transformation', 'raw_invoices.pkl')
data_path = os.path.join(f_dir, 'data', 'Online_Retail.csv')
# pd.read_excel(data_path)
def load_data(input=input_pickle_path, csv_path=data_path):
    """
    In this function we try to load the csv or the pickle
    file if it exists and save the pickle file in a 
    specific path for future use
    Args:
        pickle_path:check if the pickle file exists
        csv_path: if the pickle does not exist we load the csv file 
    return: 
        Path to the saved pickle file.
    """
    # Check if the pickle or csv file already exists and load the file into dataframe
    if os.path.exists(input):
        with open(input, "rb") as file:
            df = pickle.load(file)
        print(f"successfully load the pickle file.")
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(f"successfully load the csv file")
    else:
        error_message = "You are missing the data file"
        raise FileNotFoundError(error_message)
    # save the loaded data as pickle file
    os.makedirs(os.path.dirname(input), exist_ok=True)
    with open(input, "wb") as file:
        pickle.dump(df, file)
    print(f"Successfully save data file to {input}")
    #read the pickle file to make sure the data looks good
    with open(input,'rb') as f:
        data = pickle.load(f)
        print(data)
    return input

if __name__ == "__main__":
    unzip_f = load_data(input_pickle_path, data_path)

