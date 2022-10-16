import os
from googlesearch import *
from matplotlib.pyplot import text
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
import glob
import os
import shutil
import PyPDF2

# gebruiken voor het ophalen van de sector
from bs4 import BeautifulSoup
import requests as req

# ################# #
# Global variables #
# ################ #

url = 'https://consult.cbso.nbb.be/'


class NBBScraper():
  def findCompanyNr():
    file = 'ScrapingTools/csv/all.csv'
    df = pd.read_csv(file)
    ls = df['Ondernemingsnummer'].tolist()
    return ls


  def download_nbb(companyNr):
    # br = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
    br = webdriver.Chrome(executable_path='./chromedriver.exe')
    br.get(url)

    try:
      
      ondNrTextBox = '/html/body/app-root/div/main/div/app-deposit-search/div/p-tabview/div/div[2]/p-tabpanel[1]/div/app-search-by-enterprise-number/div/div[1]/div/input'
      ondNrButton = '/html/body/app-root/div/main/div/app-deposit-search/div/p-tabview/div/div[2]/p-tabpanel[1]/div/app-search-by-enterprise-number/div/div[2]/p-button/button'

      wait = WebDriverWait(br, 10)
      wait.until(EC.element_to_be_clickable((By.XPATH, ondNrTextBox))).send_keys(companyNr)
      
      wait = WebDriverWait(br, 10)
      wait.until(EC.presence_of_element_located((By.XPATH, ondNrButton))).click()
      
      #br.find_element(By.XPATH, ondNrButton).click()
      #br.find_element(By.XPATH, ondNrTextBox).send_keys('0431 852 314')
      

      xpathPDFDownload = '/html/body/app-root/div/main/div/app-search-result/div/div[2]/app-deposit-list/div/div[3]/app-deposit-item[1]/div/div[5]/app-download-deposit-pdf-button/button'
      xpathCSVDownload= '/html/body/app-root/div/main/div/app-search-result/div/div[2]/app-deposit-list/div/div[3]/app-deposit-item[1]/div/div[5]/app-download-deposit-csv-button/button'

      try:
        wait = WebDriverWait(br, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpathPDFDownload))).click()
      except:
        """
        TODO log uitschrijven
        """
      
      time.sleep(2)

      try:
        wait = WebDriverWait(br, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpathCSVDownload))).click()
      except:
        """
        TODO log uitschrijven
        """
        print('CSV NIET GEVONDEN')

      time.sleep(5)

    except Exception as e:
      print(e)
      print('Failed...')

    finally:
      br.quit()



  """
  nummers = findCompanyNr()
  teller = 0

  print(len(nummers))

  for nr in nummers:
    if teller > 0 and teller < 5000:
      scrapeteInfo = download_pdf(nr.replace(" ", ""))
      time.sleep(1) # Om zeker te zijn dat de file gedownload is alvorens we ze gaan verplaatsen, anders verplaatsen we een verkeerde.

      print(f'{nr} bekeken')

      #move_file()
      #delete_file() # Uncomment dit om ruimte te besparen op je HDD, maar zorg dat je eerst scrapet.
      print(teller)
    
    teller += 1
  """