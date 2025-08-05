from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from interface import Interface

class Parsing:
    def __init__(self,url,search_element):
        self.url = url
        self.search_element = search_element

    def parse_sites(self):
        self.options = Options()
        self.options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(self.options)
        self.driver.get(self.url)
        self.input = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.ID,"search"))
        )
        self.input.clear()
        self.input.send_keys(self.search_element)
        self.input.send_keys(Keys.RETURN)
        self.span = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,".css-1r6clzs span"))
        )

        self.container = WebDriverWait(self.driver,10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME,"css-1g5933j"))
        )
        self.title = []
        self.href = []
        self.price = []
        self.condition = []
        self.additional_information = []
        for cont in self.container:
            self.title.append(cont.find_element(By.CLASS_NAME,"css-1g61gc2").text)
            self.href.append(cont.find_element(By.CLASS_NAME,"css-1tqlkj0").get_attribute("href"))
            self.price.append(cont.find_element(By.CLASS_NAME,"css-uj7mm0").text)
            self.condition.append(cont.find_element(By.CSS_SELECTOR,".css-iudov9 span").text)
            self.additional_information.append(cont.find_element(By.CLASS_NAME,"css-vbz67q").text)

    def get_data(self):
        with open("Объявления.txt","w",encoding="UTF-8") as file:
            file.write(f"{self.span.text} \n")
            for t,p,h,c,a in zip(self.title,self.price,self.href,self.condition,self.additional_information):
                file.write(f"{t} || {p} || {h} || {c} || {a} \n")

interface = Interface()
data = interface.get_informations()
parse = Parsing(data[0],data[1])
parse.parse_sites()
parse.get_data()

