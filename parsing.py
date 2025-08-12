from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from interface import Interface
from selenium_stealth import stealth
from itertools import zip_longest
import time
from selector import SELECTORS
from URLS import URLS
import os
import pandas as pd
class Parsing:
    def __init__(self,url,search_element):
        self.url = url
        self.search_element = search_element
        self.driver = self.create_driver()
        self.title = []
        self.href = []
        self.price = []
        self.condition = []
        

    def save_to_excel(self):
        print(self.price)
        file_name = "Объявление.xlsx"

        if not os.path.exists("excel_file"):
            os.makedirs("excel_file")

        file_path = os.path.join("excel_file",file_name)
        self.excel_dictionary = {"Названия товара":self.title,"Цена":self.price,"Ссылка":self.href,"Доп информация":self.condition}
        self.df = pd.DataFrame(self.excel_dictionary)
        self.df.to_excel(file_path)


    def extract_item_data(self,cont,selectors):
        data = {}
        for key,selector,attr in selectors:
            try:
                element = cont.find_element(By.CSS_SELECTOR,selector)
                data[key] = element.get_attribute(attr) if attr else element.text
            except Exception:
                data[key] = ""
        return data
    
    def create_driver(self):
        options = Options()
        # options.add_argument("--headless")
        options.add_argument("window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        stealth(driver,languages=['en-US',"en","ru-RU","ru"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel(R) UHD Graphics 630",
                fix_hairline=True
                )
        return driver
    
    def parse_web(self,input,container,selectors,scroll_config=None):
        self.driver.get(self.url)
        self.driver.execute_script("document.body.style.zoom='50%'")
        self.input = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,input))
        )
        self.input.clear()
        self.input.send_keys(self.search_element)
        self.input.send_keys(Keys.RETURN)


        if scroll_config:
            self.scroll_page(**scroll_config)

        time.sleep(3)
        self.container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, container)))

        #* для узума тк есть некоое задержка изза чего элементы остаются пустым
        time.sleep(5)
        for i in range(len(self.container)):
            cont = WebDriverWait(self.driver,10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,container))
            )[i]
            try:
                item = self.extract_item_data(cont,selectors)
                self.title.append(item["title"])
                self.href.append(item["href"])
                self.price.append(item["price"])
                self.condition.append(item["condition"])
            except Exception:
                    continue



    def scroll_page(self,step=100,repeats=200,click_selector=None,delay=0.1):
        for _ in range(repeats):
            self.driver.execute_script(f"window.scrollBy(0,{step})")
            time.sleep(delay)
            if click_selector:
                try:
                    button_more = WebDriverWait(self.driver,10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,".button-more"))
                    )
                    button_more.click()
                except TimeoutException:
                    break



    def load_next_page(self):
        for _ in range(5):
            self.driver.execute_script("window.scrollBy(0,400)")
            time.sleep(2)
            self.button_more = WebDriverWait(self.driver,10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,".button-more"))
            )
            self.button_more.click()


interface = Interface()
data = interface.get_informations()

if isinstance(data,tuple):
    product = data[0]
    internet_magazin = data[1]
    is_closed = data[2]
    match internet_magazin:
        case "OLX":
            config = SELECTORS["OLX"]
            parse = Parsing(URLS["OLX_URL"],product)
            parse.parse_web(
            config["input"],
            config["container"],
            [("title",config["title"],None),
            ("href",config["href"],"href"),
            ("price",config["price"],None),
            ("condition",config["condition"],None)],
            scroll_config=config["scroll"],
            )
            parse.save_to_excel()
        
        case "UZUM":
            config = SELECTORS["UZUM"]
            parse = Parsing(URLS["UZUM_URL"],product)
            parse.parse_web(
            config["input"],
            config["container"],
            [("title",config["title"],None),
            ("href",config["href"],"href"),
            ("price",config["price"],None),
            ("condition",config["condition"],None)],
            scroll_config=config["scroll"],
            )
            parse.get_data()

        case "Яндекс маркет":
            config = SELECTORS["Яндекс маркет"]
            parse = Parsing(URLS["YANDEX_URL"],product)
            parse.parse_web(
            config["input"],
            config["container"],
            [("title",config["title"],None),
            ("href",config["href"],"href"),
            ("price",config["price"],None),
            ("condition",config["condition"],None)],
            scroll_config=config["scroll"],
            )
            parse.get_data()
        
        case "Озон":
            config = SELECTORS["Озон"]
            parse = Parsing(URLS["OZON_URL"],product)
            parse.parse_web(
            config["input"],
            config["container"],
            [("title",config["title"],None),
            ("href",config["href"],"href"),
            ("price",config["price"],None),
            ("condition",config["condition"],None)],
            scroll_config=config["scroll"],
            )
            parse.save_to_excel()


            

