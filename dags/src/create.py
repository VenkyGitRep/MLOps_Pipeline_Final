from pathlib import Path
import xlwings as xw

BASE_DIR = Path(__file__).parent.parent.parent

EXCEL_FILE = BASE_DIR/'data'/'online_retail_II.xlsx'
OUTPUT_DIR = BASE_DIR/'output'
OUTPUT_DIR.mkdir(parents=True,exist_ok=True)

def create_newfile(input = EXCEL_FILE,output = OUTPUT_DIR):
    with xw.App(visible=False) as app:
        wb = app.books.open(input)
        for sheet in wb.sheets:
            wb_new = app.books.add()
            sheet.copy(after = wb_new.sheets[0])
            wb_new.sheets[0].delete()
            wb_new.save(output/f'{sheet.name}.xlsx')
            wb_new.close()
        
# if __name__ == "__main__":
#     unzip_f = create_newfile(EXCEL_FILE, OUTPUT_DIR)