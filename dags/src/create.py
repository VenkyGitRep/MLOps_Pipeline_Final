import os
import pandas as pd

# Set base directory and file paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
EXCEL_FILE = os.path.join(BASE_DIR, 'data', 'online_retail_II.xlsx')
OUTPUT_DIR_1 = os.path.join(BASE_DIR, 'data', 'data_1.xlsx')
OUTPUT_DIR_2 = os.path.join(BASE_DIR, 'data', 'data_2.xlsx')

def create_newfile(input_file=EXCEL_FILE, output_file_1=OUTPUT_DIR_1, output_file_2=OUTPUT_DIR_2):
    """
    Function to create new Excel files from the input Excel file.
    
    Args:
        input_file (str): Path to the input Excel file.
        output_file_1 (str): Path to the first output Excel file.
        output_file_2 (str): Path to the second output Excel file.
        
    Returns:
        tuple: Paths to the created output Excel files.
    """
    # Read the input Excel file
    xl = pd.ExcelFile(input_file)
    
    # Read data from the first sheet and save to output_file_1
    df_1 = pd.read_excel(xl, sheet_name=xl.sheet_names[0])
    df_1.to_excel(output_file_1)
    
    # Read data from the second sheet and save to output_file_2
    df_2 = pd.read_excel(xl, sheet_name=xl.sheet_names[1])
    df_2.to_excel(output_file_2)
   
    return output_file_1, output_file_2

if __name__ == "__main__":
    # Call the function with default arguments
    created_files = create_newfile()
