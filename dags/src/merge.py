import glob
import pandas as pd
import os

# Set the base directory and input/output paths
f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
fin_path = os.path.join(f_dir, 'data')  # Input directory containing Excel files
fout_path = os.path.join(f_dir, 'data')  # Output directory to save the merged CSV file

def merg_files(input_path=fin_path, output_path=fout_path):
    """
    Function to merge multiple Excel files into a single CSV file.
    
    Args:
        input_path (str): Path to the directory containing the input Excel files.
        output_path (str): Path to the directory where the merged CSV file will be saved.
    """
    # Find all Excel files in the input directory
    file_list = glob.glob(f'{input_path}/data*.xlsx')
    
    # Initialize an empty list to store dataframes
    excel_list = []
    
    # Iterate over each file in the file list
    for file in file_list:
        # Read the Excel file and append its dataframe to the list
        excel_list.append(pd.read_excel(file))
    
    # Concatenate all dataframes into a single dataframe
    excel_merged = pd.concat(excel_list, ignore_index=True)
    
    # Save the merged dataframe as a CSV file in the output directory
    excel_merged.to_csv(f'{output_path}/Online_Retail.csv')

if __name__ == "__main__":
    # Execute the merge_files function with default input/output paths
    merg_files()
