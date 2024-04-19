import zipfile
import os

# Set the root directory variable using a relative path
file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
zip_name = os.path.join(file_dir, 'data','online_retail_II.zip')
new_name = os.path.join(file_dir, 'data','Online_Retail.xlsx')
fout_path = os.path.join(file_dir,'data')

def unzip(filename=zip_name, output_path=fout_path):
    """
    Function to unzip the downloaded data
    Args:
      zip_filename: zipfile path, a default is used if not specified
      extract_to: Path where the unzipped and extracted data is available
    Returns:
      unzipped_file: filepath where the data is available
    """
    try:
        with zipfile.ZipFile(filename, 'r') as zf:
            zf.extractall(output_path)
            # os.rename(f'{fout_path}/Online Retail.xlsx',new_name)

        print(f"File {filename} successfully unzipped to {output_path}")
    except zipfile.BadZipFile:
        print(f"Failed to unzip {filename}")
    output_file =  os.path.join(output_path, 'Online_Retail_II.xlsx')
    return output_file

if __name__ == "__main__":
    unzip_f = unzip(zip_name, fout_path)