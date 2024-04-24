import os
import requests

url = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zidp"

def download_file(file_url=url):
    """
    This function is for us to download the dataset from kaggle or anywhere else you want and automate
    the download process in the datapipeline
    Args:
        file_path (str): default http link from kaggle and you can define whatever link you want.
    Return:
        zipfile_path(str): The path you save your zip file
    """
    downloaded = requests.get(file_url, timeout=100)
    print(f'your file from {downloaded} is downloading please wait for 100 secs.')
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'data')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
    zipfile_path=os.path.join(root_dir, 'data','Online_Retail_II.zip')
    #see if the request is successful
    if downloaded.status_code == 200:
        with open(zipfile_path, "wb") as file:
            file.write(downloaded.content)
        print(f"Your file has downloaded in {zipfile_path}")
    else:
        print(f"Your file has failed to download please recheck")

    return zipfile_path

if __name__ == "__main__":
    zip_path = download_file("https://archive.ics.uci.edu/static/public/502/online+retail+ii.zfip")
    