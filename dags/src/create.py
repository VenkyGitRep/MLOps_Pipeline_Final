import os
import pandas as pd
from pathlib import Path

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
EXCEL_FILE = os.path.join(BASE_DIR, 'data','online_retail_II.xlsx')
OUTPUT_DIR_1 = os.path.join(BASE_DIR, 'data','data_1.xlsx')
OUTPUT_DIR_2 = os.path.join(BASE_DIR, 'data','data_2.xlsx')



def create_newfile(input = EXCEL_FILE,output_1 = OUTPUT_DIR_1,output_2 = OUTPUT_DIR_2):
   xl = pd.ExcelFile(input)
   xl.sheet_names[0]
   df_1 = pd.read_excel(xl,sheet_name=xl.sheet_names[0])
   df_1.to_excel(output_1)
   df_2 = pd.read_excel(xl,sheet_name=xl.sheet_names[1])
   df_2.to_excel(output_2)
   
   return output_1, output_2
if __name__ == "__main__":
    unzip_f = create_newfile(EXCEL_FILE, OUTPUT_DIR_1, OUTPUT_DIR_2)