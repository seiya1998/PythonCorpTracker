from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from typing import Tuple

class DentalClinicTracker:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.driver.implicitly_wait(2)

    def move_page(self) -> None:
        self.driver.find_element(By.XPATH, '//*[contains(text(), "ドクターズ・ファイル")]').click()

    def get_contents(self) -> list:
        urls = []
        contents = []
        results = self.driver.find_elements(By.CLASS_NAME, 'result')
        for result in results:
            urls.append(result.find_element(By.CLASS_NAME, 'result__name').get_attribute('href'))

        # while True:
        #     # 現在のURL（一覧）を取得
        #     current_url = self.driver.current_url

        #     # 次へボタンののクラスを取得
        #     next_page_class = self.driver.find_element(By.CLASS_NAME, 'pagination__next').get_attribute('class')

        #     # 次へボタンのクラスに「is-disabled」があれば終わり
        #     if 'is-disabled' in next_page_class:
        #         break
        #     else:
        #         results = self.driver.find_elements(By.CLASS_NAME, 'result')
        #         for result in results:
        #             urls.append(result.find_element(By.CLASS_NAME, 'result__name').get_attribute('href'))
                
        #         # 次へクリック
        #         self.driver.get(current_url)
        #         self.driver.find_element(By.CLASS_NAME, 'pagination__next').click()

        for index, result in enumerate(urls, 1):
            self.driver.get(result)
            name = self.get_content_by_xpath('//*[@id="info"]/table/tbody/tr[1]/td')
            tel = self.get_content_by_xpath('//*[@id="info"]/table/tbody/tr[4]/td')
            address = self.get_content_by_xpath('//*[@id="info"]/table/tbody/tr[5]/td')
            url = self.get_content_by_xpath('//*[@id="info"]/table/tbody/tr[6]/td')
            contents.append([index, name, url, address, tel])

        return contents

    def get_content_by_xpath(self, xpath: str) -> Tuple[str, None]:
        try:
            content = self.driver.find_element(By.XPATH, xpath)
            return content.text
        except Exception as e:
            return None