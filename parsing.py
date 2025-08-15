from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from interface import Interface
from selenium_stealth import stealth
import time
from selector import SELECTORS
import os
import pandas as pd
from stylized_excel import styling_excel
from openpyxl.utils.dataframe import dataframe_to_rows
import openpyxl


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
        file_name = "Объявление.xlsx"
        folder = "excel_file"

        if not os.path.exists(folder):
            os.makedirs("excel_file")


        file_path = os.path.join(folder,file_name)
        excel_dictionary= {"Названия товара":self.title,"Цена":self.price,"Ссылка":self.href,"Доп информация":self.condition}
        df = pd.DataFrame(excel_dictionary)

        if os.path.isfile(file_path):
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook["Sheet1"]
            for row in dataframe_to_rows(df,index=False,header=False):
                sheet.append(row)

            workbook.save(file_path)
            workbook.close()
            styling_excel(file_path)
        else:
            df.to_excel(file_path,index=False)
            styling_excel(file_path)
        
        self.driver.close()
        
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
        service = Service(log_output=os.devnull)
        options = Options()
        options.add_experimental_option("excludeSwitches",['enable-logging'])
        options.add_argument("--log-level=3")
        options.add_argument("--silent") 
        options.add_argument("--headless")
        options.add_argument("window-size=1920,1080")
        driver = webdriver.Chrome(service=service,options=options)
        stealth(driver,languages=['en-US',"en","ru-RU","ru"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel(R) UHD Graphics 630",
                fix_hairline=True
                )
        return driver
    
    def parse_web(self,input,price_filter,price,container,selectors,scroll_config=None):
        print("Идет парсинг...")
        self.driver.get(self.url)
        self.driver.execute_script("document.body.style.zoom='50%'")
        self.input = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,input))
        )
        self.input.clear()
        self.input.send_keys(self.search_element)
        self.input.send_keys(Keys.RETURN)


        filter_price = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.XPATH,price_filter))
        )

        if not self.url == "https://uz.ozon.com/":
            if price != 0:
                filter_price.clear()
                filter_price.send_keys(price)
                filter_price.send_keys(Keys.RETURN)

        if scroll_config:
            self.scroll_page(**scroll_config)

        time.sleep(3)
        self.container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, container)))


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
                    EC.element_to_be_clickable((By.CSS_SELECTOR,click_selector))
                    )
                    button_more.click()
                except TimeoutException:
                    break

    


interface = Interface()
data = interface.get_informations()

if isinstance(data,tuple) and len(data) == 3:
    product = data[1]
    price = data[2]
    for sites in SELECTORS:
        config = SELECTORS[sites]
        parse = Parsing(config["URL"],product)
        parse.parse_web(config['input'],config["price_filter"],price,config['container'],[
            ("title",config["title"],None),
            ("href",config["href"],"href"),
            ("price",config["price"],None),
            ("condition",config["condition"],None)
            ],scroll_config=config["scroll"])

        parse.save_to_excel()


elif isinstance(data,tuple):
    product = data[0]
    internet_magazin = data[1]
    is_closed = data[2]
    price = data[3]
    match internet_magazin:
        case "OLX":
            config = SELECTORS["OLX"]
            parse = Parsing(config["URL"],product)
            parse.parse_web(
            config["input"],
            config["price_filter"],
            price,
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
            parse = Parsing(config["URL"],product)
            parse.parse_web(
            config["input"],
            config['price_filter'],
            price,
            config["container"],
            [("title",config["title"],None),
            ("href",config["href"],"href"),
            ("price",config["price"],None),
            ("condition",config["condition"],None)],
            scroll_config=config["scroll"],
            )
            parse.save_to_excel()

        case "Яндекс маркет":
            config = SELECTORS["Яндекс маркет"]
            parse = Parsing(config["URL"],product)
            parse.parse_web(
            config["input"],
            config['price_filter'],
            price,
            config["container"],
            [("title",config["title"],None),
            ("href",config["href"],"href"),
            ("price",config["price"],None),
            ("condition",config["condition"],None)],
            scroll_config=config["scroll"],
            )
            parse.save_to_excel()

    


            

