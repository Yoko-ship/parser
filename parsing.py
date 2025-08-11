from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from interface import Interface
from selenium_stealth import stealth
from itertools import zip_longest
import time

OLX_URL = "https://www.olx.uz/"
UZUM_URL = "https://uzum.uz/ru" 
YANDEX_URL = "https://market.yandex.uz/"
OZON_URL = "https://uz.ozon.com/"

class Parsing:
    def __init__(self,url,search_element):
        self.url = url
        self.search_element = search_element

    def get_data(self):
        with open("Объявления.txt","w",encoding="UTF-8") as file:
            for t,p,h,c in zip_longest(self.title,self.price,self.href,self.condition,fillvalue=""):
                file.write(f"{t} || {p} || {h} || {c}  \n")
            print("Товары успешно добавлены в Объявления.txt")


    def parse_web(self,input,container,title,href,price,condition):
        self.options = Options()
        self.options.add_argument("window-size=1920,1080")
        self.driver = webdriver.Chrome(options=self.options)
        stealth(self.driver,languages=['en-US',"en","ru-RU","ru"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel(R) UHD Graphics 630",
                fix_hairline=True
                )
        self.driver.get(self.url)
        self.input = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,input))
        )
        self.input.clear()
        self.input.send_keys(self.search_element)
        self.input.send_keys(Keys.RETURN)


        self.title = []
        self.href = []
        self.price = []
        self.condition = []
        
        if self.url == OZON_URL or self.url == YANDEX_URL:
            self.scroll_page()

        elif self.url == UZUM_URL:
            self.load_next_page()
        
        time.sleep(3)
        self.container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, container)))

        #* для узума тк есть некоое задержка изза чего элементы остаются пустым
        if self.url == UZUM_URL or self.url == YANDEX_URL:
            time.sleep(5)
            for i in range(len(self.container)):
                cont = WebDriverWait(self.driver,10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR,container))
                )[i]
                try:
                    self.title.append(cont.find_element(By.CSS_SELECTOR, title).text)
                    self.href.append(cont.find_element(By.CSS_SELECTOR, href).get_attribute("href"))
                    self.price.append(cont.find_element(By.CSS_SELECTOR, price).text)
                    self.condition.append(cont.find_element(By.CSS_SELECTOR, condition).text)
                except Exception:
                    continue
        else:
            for cont in self.container:
                try:
                    self.title.append(cont.find_element(By.CSS_SELECTOR, title).text)
                    self.href.append(cont.find_element(By.CSS_SELECTOR, href).get_attribute("href"))
                    self.price.append(cont.find_element(By.CSS_SELECTOR, price).text)
                    self.condition.append(cont.find_element(By.CSS_SELECTOR, condition).text)
                except Exception:
                    continue


    def scroll_page(self):
        for _ in range(200):
            self.driver.execute_script("window.scrollBy(0,100)")
            time.sleep(0.1)



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
            parse = Parsing(OLX_URL,product)
            parse.parse_web("#search",".css-1g5933j",".css-1g61gc2",".css-1tqlkj0",".css-uj7mm0",".css-iudov9 span")
            parse.get_data()
        
        case "UZUM":
            parse = Parsing(UZUM_URL,product)
            parse.parse_web(".input-line input","#category-products > div",".product-card__title","[data-test-id='product-card--default']",".currency",".reviews")
            parse.get_data()


        case "Яндекс маркет":
            parse = Parsing(YANDEX_URL,product)
            parse.parse_web("#header-search","[data-auto='SerpList'] > div, [data-auto='SerpGrid'] > div","[data-auto='snippet-title']",".EQlfk","[data-auto='snippet-price-current']","[data-baobab-name='rating'] > *:first-child")
            parse.get_data()
        
        case "Озон":
            parse = Parsing(OZON_URL,product)
            parse.parse_web(".tr8_31",".i7u_24 > div",".bq02_5_0-a span",".q4b1_3_0-a",".c35_3_2-a0 > *:first-child",".p6b2_5_0-a4 > *:nth-child(2)")
            parse.get_data()

            

