import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))

fin_path = os.path.join(f_dir, 'data', 'transformation','outliers.pkl')
train_path = os.path.join(f_dir, 'data', 'transformation','data_train.pkl')
test_path = os.path.join(f_dir, 'data', 'transformation','data_test.pkl')

def split_data(input = fin_path, output_train = train_path, output_test = test_path, prop = 0.2):
    """This function is for us to split the data into train and test files and save them for the 
    future using.

    Args:
        input (str): the data file path from the outliers handler
        output_train (str): file path that the train data set is going to be stored in
        output_test (str): file path that the test data set is going to be stored in
        prop (float): the test/train's proportion Defaults to 0.2.
    """
    if os.path.exists(input):
        with open(input, "rb") as f:
            df = pickle.load(f)
    else:
        raise FileNotFoundError()
    
    training_data, testing_data = train_test_split(df, test_size=0.2, random_state=25)
    
    with open(output_train, 'wb') as file_train:
        pickle.dump(training_data, file_train) 
    with open(output_test,'wb') as file_test:
        pickle.dump(testing_data,file_test)
    #print out the data to see the structure
    with open(output_train, 'rb') as f:
        data = pickle.load(f)
        print(data)
    with open(output_test, 'rb') as f:
        data = pickle.load(f)
        print(data)
    return output_train,output_test

# if __name__ == "__main__":
#     unzip_f = split_data(fin_path, train_path,test_path)