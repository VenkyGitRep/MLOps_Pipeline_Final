import glob
import pandas as pd
import os


f_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))

fin_path = os.path.join(f_dir, 'output')
fout_path = os.path.join(f_dir, 'data')

def merg_files(input = fin_path,output = fout_path):
    file_list = glob.glob(f'{input}/*.xlsx')
    print("file_list:",file_list)
    excel_list = []
    for file in file_list:
        excel_list.append(pd.read_excel(file))
    print(len(excel_list))
    if(len(excel_list)>0):
        excel_merged = pd.concat(excel_list,ignore_index=True)
        excel_merged.to_csv(f'{output}/Online_Retail.csv')

    
if __name__ == "__main__":
    unzip_f = merg_files(fin_path,fout_path)
    