import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import os
import subprocess

subprocess.Popen(r"D:\aligrosir_chrome_data\run_chrome.bat", cwd=r"C:\Program Files\Google\Chrome\Application")
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:8989")
driver = webdriver.Chrome(options=options)
delay_time = 15
image_path = r"D:\best500"
description_file = open(r"D:\best500\description.txt", "r")
description = description_file.read()

description_file.close()
driver.maximize_window()
driver.get("https://seller.tokopedia.com/statistic/products")
for times in range(10):
    driver.implicitly_wait(delay_time)
    driver.find_element(By.CSS_SELECTOR, "#analysis-tab").click()
    driver.implicitly_wait(delay_time)
    driver.execute_script("window.scrollTo(0, 250);")
    driver.implicitly_wait(delay_time)
    # Select the first product in the list
    driver.find_element(By.CSS_SELECTOR, f"#productAnalysisFields-col-0-1").click()
    try:
        # Check if the product is not completed
        driver.implicitly_wait(delay_time)
        driver.find_element(By.XPATH, '//*[@id="post-undefined"]/div/div[1]/div[1]/p')
        # Edit product button
        driver.implicitly_wait(delay_time)
        driver.find_element(By.XPATH, '//*[@id="post-undefined"]/div/a').click()
        # Switch to new tab
        driver.switch_to.window(driver.window_handles[1])
        driver.implicitly_wait(delay_time)
        driver.find_element(By.CSS_SELECTOR, "#merchant-root > div > div.content-container > div > div.css-1fqmeth > section > div.css-56v2xt.ege6ygj0 > svg").click()
        # Product name
        driver.implicitly_wait(delay_time)
        try:
            product_name_el = driver.find_element(By.XPATH, '//*[@id="infoSection-title"]/div[2]/div/div[1]/div/div[1]/div/input')
            product_name = product_name_el.get_attribute("value")
            if len(product_name) < 40 <= len(product_name + f" original") and len(product_name.split()) >= 2:
                print("Product name's less than 40")
                new_product_name = " ".join(product_name.split()[:2])
                print(f"new_product_name: {new_product_name}")
                product_name_el.send_keys(Keys.CONTROL + 'a')
                product_name_el.send_keys(Keys.DELETE)
                product_name_el.send_keys(new_product_name)
                driver.implicitly_wait(delay_time)
                product_names_tab = list(e.text for e in driver.find_elements(By.XPATH, '//*[@id="infoSection-title"]/div[2]/div/div[2]/p'))
                product_name_el.send_keys(Keys.CONTROL + 'a')
                product_name_el.send_keys(Keys.DELETE)
                product_name_el.send_keys(sorted(product_names_tab, key=len)[-1]+" original") if len(sorted(product_names_tab,key=len)[-1]+" original") <= 100 else product_name_el.send_keys(sorted(product_names_tab, key=len)[-1])
        except Exception as err:
            print(f"ERROR BRO: {err}")
        time.sleep(delay_time)
        driver.execute_script("window.scrollTo(0, 1100);")
        # Upload images
        img_files = list((fr"{image_path}\{file_name}" for file_name in os.listdir(f"{image_path}") if
                          file_name.endswith(".jpg") or file_name.endswith(".png")))
        driver.implicitly_wait(delay_time)
        img = driver.find_element(By.CSS_SELECTOR, "#imgInputEl")
        img.send_keys("\n".join(img_files))
        driver.execute_script("window.scrollTo(0, 1500);")
        # Add description if appropiate
        driver.implicitly_wait(delay_time)
        input_description = driver.find_element(By.XPATH, '//*[@id="desc-analysis"]/div[2]/div[1]/textarea')
        if len(input_description.text) + len(f"\n\n{description}") <= 2000: input_description.send_keys(
            f"\n\n{description}") if len(input_description.text) != 0 else input_description.send_keys(f"{description}")
        for t in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        # Save all changes
        driver.implicitly_wait(delay_time)
        driver.find_element(By.XPATH, '//*[@id="merchant-root"]/div/div[2]/div/div[2]/button[3]').click()
        time.sleep(delay_time)
        current_tab = driver.current_window_handle
        for tab in driver.window_handles:
            driver.switch_to.window(tab)
            if current_tab != tab:
                driver.close()
        driver.refresh()
    except NoSuchElementException as err:
        print(err)
        continue
