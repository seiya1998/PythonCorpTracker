from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import csv
from dental_clinic_tracker import DentalClinicTracker
from salon_tracker import SalonTracker
from hair_removal_salon_tracker import HairRemovalSalonTracker


class CorpTracker:
    def __init__(self, prefecture: str, industry: int) -> None:
        self.prefecture = prefecture
        self.industry = industry
        driver_path = ChromeDriverManager().install()
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(executable_path=driver_path, chrome_options=chrome_options))
        self.driver.implicitly_wait(2)
        self.industries = {
            1: '歯科',
            2: 'クリニック、病院',
            3: '美容室',
            4: 'ネイルサロン',
            5: 'まつ毛サロン',
            6: 'エステサロン',
            7: '脱毛',
            8: '日焼けサロン',
            9: '食事',
        }
    

    def search_by_google(self) -> None:
        self.driver.get('https://www.google.com/')
        search = self.driver.find_element(By.NAME, "q")
        search.send_keys(f"{self.prefecture} {self.industries[self.industry]}一覧") 
        search.submit()

        if self.industry == 1:
            tracker = DentalClinicTracker(self.driver)
        elif self.industry == 3:
            tracker = SalonTracker(self.driver)
        elif self.industry == 4:
            tracker = SalonTracker(self.driver)
        elif self.industry == 5:
            tracker = SalonTracker(self.driver)
        elif self.industry == 6:
            tracker = SalonTracker(self.driver)
        elif self.industry == 7:
            tracker = HairRemovalSalonTracker(self.driver)

        tracker.move_page()
        contents = tracker.get_contents()
        self.generate_result_csv(contents)
        

    def generate_result_csv(self, rows: list) -> str:
        header = ['', '店名', 'URL', '住所', '電話番号']
        with open(f'csv/{self.prefecture}_{self.industries[self.industry]}一覧.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)


if __name__ == "__main__":
    prefecture = input('都道府県を入力してください。')
    industry = int(input('業種を入力してください。 1: 歯科, 3: 美容室　：'))
    tracket = CorpTracker(prefecture, industry)
    tracket.search_by_google()