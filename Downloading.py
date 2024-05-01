import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd 
import glob

# Function to check if the download is still in progress
def is_download_finished(download_path, file_name):
 file_path = os.path.join(download_path,file_name)
 return os.path.exists(file_path)

#File path with URLs
file_path = r'D:\Elivation\TanDEM-X 30m DEM Change Map (DCM)\Saudi Arabia\TDM30_DCM-url-list (1).txt'

#Open the file containing URLs
f = open(file_path, "r")
file_contents = f.read()
df= pd.DataFrame(file_contents.split(),columns=["URL"])
df["basename"]=df['URL'].apply(lambda x: os.path.basename(x))
download_path= os.path.join(os.path.expanduser('~'),'Downloads')

files_list = os.listdir(download_path)

files_list= [i for i in os.listdir(download_path)if i.endswith(".zip")]
files_list_2=pd.DataFrame(files_list)


files_list_2.columns= ["basename_2"]

merged_df = pd.merge(df,files_list_2, left_on='basename', right_on='basename_2', how='left')
merged_df['basename_2'].fillna(0,inplace=True)
merged_data=merged_df[merged_df['basename_2']==0]
merged_data=pd.DataFrame(merged_data)

#Initialize web driver
chrome_options = Options()
chrome_options.add_experimental_option("detach",True)

for index, row in merged_data.iterrows():
    column1_value = row['URL']
    driver = webdriver.Chrome(options=chrome_options)
    url = column1_value.strip()

    driver.get(url)

    # Find the username input field by ID and input username
    username_field = driver.find_element(By.ID,"username")
    username_field.send_keys("AahlaadMusunuru1995")

    # Find the password input field by ID and input password
    password_field = driver.find_element(By.ID,"password")
    password_field.send_keys("wKq6#pA3Ixh8*n5l")

    # Find and click the login button using XPath
    login_button = driver.find_element(By.XPATH,"//button[@value='Login']")
    login_button.click()

    # Get the default Downloads folder path for Windows
    download_path = os.path.join(os.path.expanduser('~'),'Downloads')

    # Wait for download to complete

    file_name = os.path.basename(url)# Specify the download file name
    while not is_download_finished(download_path, file_name):
        time.sleep(1)# Check every second

        # Close Chrome after the download is complete for each URL
    driver.quit()
