from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

processed_pan_numbers = set()
data_list=[]

try:
    driver.get('https://hprera.nic.in/PublicDashboard')

    wait = WebDriverWait(driver, 130)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[title='View Application']")))


    for i in range(6):
        links = driver.find_elements(By.CSS_SELECTOR, "a[title='View Application']")
        
        if i >= len(links):
            print("No more links found.")
            break

        try:
            links[i].click()
            time.sleep(2)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.mb-3")))

            soup = BeautifulSoup(driver.page_source, "lxml")
            table_data = {}
            rows = soup.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                if len(cells) == 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    table_data[key] = value
                elif len(cells) == 3:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip() + " " + cells[2].text.strip()
                    table_data[key] = value

            name = table_data.get('Name', 'Not Found')
            pan_no = table_data.get('PAN No.', 'Not Found')
            gstin_no = table_data.get('GSTIN No.', 'Not Found')
            permanent_address = table_data.get('Permanent Address', 'Not Found')

            if pan_no in processed_pan_numbers:
                print(f"Duplicate record for PAN No.: {pan_no} - Skipping")
                close_button = driver.find_element(By.CSS_SELECTOR, "button.close")
                close_button.click()
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[title='View Application']")))
                continue

            processed_pan_numbers.add(pan_no)

            print(f"Information from link {i+1}:")
            print(f"Name: {name}")
            print(f"PAN No.: {pan_no}")
            print(f"GSTIN No.: {gstin_no}")
            print(f"Permanent Address: {permanent_address}")
            print("\n")

            data_list.append({
                "GSTIN No.": gstin_no,
                "PAN No.": pan_no,
                "Name": name,
                "Permanent Address": permanent_address
            })
            
            close_button = driver.find_element(By.CSS_SELECTOR, "button.close")
            close_button.click()
            
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[title='View Application']")))

        except Exception as e:
            print(f"Exception occurred for link {i+1}: {e}")
            driver.get('https://hprera.nic.in/PublicDashboard')
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[title='View Application']")))

finally:

    driver.quit()


df = pd.DataFrame(data_list)

df['PAN No.'] = df['PAN No.'].str.replace(r'\nPAN File', '', regex=True).str.strip()
df['GSTIN No.'] = df['GSTIN No.'].str.replace(r'\nGST Certificate', '', regex=True).str.strip()

print(df)
df.to_csv('extract.csv',index=False)
