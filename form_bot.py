import time
import threading
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import gspread
from google.oauth2.service_account import Credentials


#logging.basicConfig(level=logging.INFO)

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("D:/python/pythonbot/bot-sheet-438808-de838a16ee8f.json", scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "1L6qYiIbFBQPMBC3-EPCD37uLpIbNUNyysTjfV45eG-o"
sheet = client.open_by_key(sheet_id)
data = sheet.sheet1.get_all_values()

def fill_form(row, row_index):
    logging.info(f"Processing row {row_index + 1}: {row}")
    name = row[0]
    email = row[1]
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled') 
    driver = None
    try:
        driver = webdriver.Chrome(options=options)
        driver.get('https://tally.so/r/waDMG2')
        logging.info("Page loaded")
        time.sleep(5)  
        try:
            name_field = driver.execute_script("return document.getElementById('e729bd5e-3362-4712-823c-9b426dcb0610')")
            if name_field:
                logging.info("Name field located")
            else:
                logging.error("Could not locate name field")
                return
        except Exception as e:
            logging.error(f"Exception locating name field: {e}")
            return
        try:
            email_field = driver.execute_script("return document.getElementById('9271d54a-c70b-4375-ac4b-7ad4502d321d')")
            if email_field:
                logging.info("Email field located via JavaScript")
            else:
                logging.error("Could not locate email field via JavaScript")
                return
        except Exception as e:
            logging.error(f"Exception locating email field: {e}")
            return
        try:
            submit_button = driver.execute_script("return document.querySelector('button[type=\"submit\"][value=\"done\"]')")
            if submit_button:
                logging.info("Submit button located")
            else:
                logging.error("Could not locate submit button")
                return
        except Exception as e:
            logging.error(f"Exception locating submit button: {e}")
            return
        logging.info(f"Filling form with Name: {name}, Email: {email}")
        try:
            name_field.send_keys(name)
            email_field.send_keys(email)
            logging.info("Fields filled successfully")
        except Exception as e:
            logging.error(f"Exception filling fields: {e}")
            return
        try:
            submit_button.click()
            WebDriverWait(driver, 40).until(EC.url_changes('https://tally.so/r/waDMG2'))
            logging.info("Form submitted successfully")
        except Exception as e:
            pass 
        sheet.sheet1.update_cell(row_index + 1, 3, "Done")
        logging.info(f"Successfully submitted row {row_index + 1}")
    except WebDriverException as e:
        logging.error(f"WebDriverException: {e}")
    finally:
        if driver:
            driver.quit()
def worker(row_index):
    try:
        row = data[row_index]
        if len(row) >= 2:
            fill_form(row, row_index)
        else:
            logging.warning(f"Skipping row {row_index + 1}: Not enough data")
    except Exception as e:
        logging.error(f"Error processing row {row_index + 1}: {e}")
def main():
    while True:
        try:
            start_row = int(input("Enter the start row: "))
            if start_row > 0:
                break
            else:
                logging.error("Start row must be greater than 0.")
        except ValueError:
            logging.error("Please enter a valid number.")
    num_threads = int(input("Enter the number of threads: "))
    threads = []
    for row_index in range(start_row - 1, len(data)):
        thread = threading.Thread(target=worker, args=(row_index,))
        threads.append(thread)
        thread.start()
        if len(threads) >= num_threads:
            for thread in threads:
                thread.join()
            threads = []

if __name__ == '__main__':
    main()
