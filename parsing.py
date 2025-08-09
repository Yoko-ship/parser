from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from interface import Interface
import time
class Parsing:
    def __init__(self,url,search_element):
        self.url = url
        self.search_element = search_element

    def get_data(self):
        with open("Объявления.txt","w",encoding="UTF-8") as file:
            # file.write(f"{self.span.text} \n")
            for t,p,h,c in zip(self.title,self.price,self.href,self.condition):
                file.write(f"{t} || {p} || {h} || {c}  \n")
            
            print("Товары успешно добавлены в Объявления.txt")


    def parse_web(self,input,span,container,title,href,price,condition):
        self.options = Options()
        self.options.add_argument("window-size=1920,1080")
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.url)
        self.input = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,input))
        )
        self.input.clear()
        self.input.send_keys(self.search_element)
        self.input.send_keys(Keys.RETURN)
        # self.span = WebDriverWait(self.driver,10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR,span))
        # )

        self.title = []
        self.href = []
        self.price = []
        self.condition = []
        
        self.container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, container))
        )
        
        for cont in self.container:
            try:
                self.title.append(cont.find_element(By.CSS_SELECTOR, title).text)
                self.href.append(cont.find_element(By.CSS_SELECTOR, href).get_attribute("href"))
                self.price.append(cont.find_element(By.CSS_SELECTOR, price).text)
                self.condition.append(cont.find_element(By.CSS_SELECTOR, condition).text)
            except Exception:
                continue

interface = Interface()
data = interface.get_informations()

if isinstance(data,tuple):
    product = data[0]
    internet_magazin = data[1]
    is_closed = data[2]
    match internet_magazin:
        case "OLX":
            parse = Parsing("https://www.olx.uz/",product)
            parse.parse_web("#search",".css-1r6clzs span",".css-1g5933j",".css-1g61gc2",".css-1tqlkj0",".css-uj7mm0",".css-iudov9 span")
            parse.get_data()
        
        case "UZUM":
            parse = Parsing("https://uzum.uz/ru",product)
            parse.parse_web(".input-line input",".title h1 span","#category-products > div",".product-card__title","[data-test-id='product-card--default']",".currency",".reviews")
            parse.get_data()


        case "Яндекс маркет":
            parse = Parsing("https://market.yandex.uz/",product)
            parse.parse_web("#header-search","","[data-auto='SerpGrid'] > div","[data-auto='snippet-title']",".EQlfk","[data-auto='snippet-price-current']","[data-baobab-name='rating'] > *:first-child")
            parse.get_data()


