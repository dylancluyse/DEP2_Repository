import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Controllers.Repositories.AnnualReports_Repository import AnnualReportsRepo as arr

# gebruiken voor het ophalen van de sector


# ################# #
# Global variables #
# ################ #
url = 'https://consult.cbso.nbb.be/'


class NBBScraper():

  """
  TODO ...
  """
  def add_nbb_contents(compnr, companyname):
      arr.add_NBB_CSV()
      arr.add_NBB_PDF(companyNr=compnr, companyname=companyname)

  def download_nbb(companyNr):
    options = webdriver.ChromeOptions()
    dirToPrint=os.getcwd()+'\Storage'
    prefs={"download.default_directory":dirToPrint}
    options.add_experimental_option("prefs",prefs)

    br = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)


    br.get(url)

    try:

      ondNrTextBox = '/html/body/app-root/div/main/div/app-deposit-search/div/p-tabview/div/div[2]/p-tabpanel[1]/div/app-search-by-enterprise-number/div/div[1]/div/input'
      ondNrButton = '/html/body/app-root/div/main/div/app-deposit-search/div/p-tabview/div/div[2]/p-tabpanel[1]/div/app-search-by-enterprise-number/div/div[2]/p-button/button'

      wait = WebDriverWait(br, 10)
      wait.until(EC.element_to_be_clickable((By.XPATH, ondNrTextBox))).send_keys(companyNr)

      wait = WebDriverWait(br, 10)
      wait.until(EC.presence_of_element_located((By.XPATH, ondNrButton))).click()

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

