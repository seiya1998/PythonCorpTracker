from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from typing import Tuple

class HairRemovalSalonTracker:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.driver.implicitly_wait(2)

    def move_page(self) -> None:
        self.driver.find_element(By.XPATH, '//*[contains(text(), "ホットペッパービューティー")]').click()

    def get_contents(self) -> list:
        urls = []
        contents = []

        while True:
            element = self.driver.find_element(By.CLASS_NAME, 'slnCassetteList')
            salons = element.find_elements(By.TAG_NAME, "li")
            for salon in salons:
                urls.append(salon.find_element(By.XPATH, '/div[1]/h3/a').get_attribute('href'))
            
            # ページネーションの次へボタンがある場合
            if len(self.driver.find_elements(By.CLASS_NAME, 'afterPage')) > 0:
                self.driver.find_element(By.CLASS_NAME, 'afterPage').click()
            else:
                break

        
        for index, result in enumerate(urls, 1):
            self.driver.get(result)
            current_url = self.driver.current_url
            try:
                content = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainContents"]/div[7]/table/tbody/tr[1]/td/a')))
                content.click()
                tel = self.get_content_by_xpath('//*[@id="mainContents"]/table/tbody/tr/td').text
                self.driver.get(current_url)
            except Exception as e:
                tel = None
            name = self.driver.find_element(By.XPATH, '//*[@id="mainContents"]/div[1]/div/div[3]/div/p[1]/a').text
            address = self.get_content_by_xpath('//*[@id="mainContents"]/div[7]/table/tbody/tr[2]/td').text
            url = self.get_content_by_xpath('//*[@id="store_hp"]').text
            contents.append([index, name, url, address, tel])

        return contents

    def get_content_by_xpath(self, xpath: str) -> Tuple[str, None]:
        try:
            content = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return content.text
        except Exception as e:
            return None