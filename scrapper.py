from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

from bs4 import BeautifulSoup


class Product(object):
    def __init__(self, title, quantity, price):
        self.title = title
        self.price = price
        self.quantity = quantity

driver = webdriver.Chrome()
driver.get('https://tienda.mercadona.es/authenticate-user')

# Codig postal
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/div[5]/div[2]/div[2]/form/div/input"))).send_keys("08001")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/div[5]/div[2]/div[2]/form/button"))).click()

# Identificacio pagina
try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/header/div[2]/div/div/button"))).click()
catch:
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/header/div[2]/div/div/button"))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/header/div[2]/div/div/div/div/a[1]"))).click()

# login
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/div[2]/div[2]/div/div[2]/div[2]/div[3]/form/div/input"))).send_keys("oussamarakye@gmail.com")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/div[2]/div[2]/div/div[2]/div[2]/div[3]/form/button[1]"))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/div[2]/div[2]/div/div[2]/div[2]/div[3]/form/div/div/input"))).send_keys("dof12ineT")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"root\"]/div[2]/div[2]/div/div[2]/div[2]/div[3]/form/button[2]"))).click()

list_products = []
letters = 'abcdefghijklmnopqrstuvwxyz'

for letter in letters:
    for l in letters:
        for e in letters:
            driver.get('https://tienda.mercadona.es/search-results?query=' + letter + l + e)

            sleep(0.25)

            html = driver.page_source

            soup = BeautifulSoup(html, 'lxml')

            for tag in soup.find_all('div', 'product-cell'):
                list_products.append(Product(
                    title=tag.find('h4', "subhead1-r product-cell__description-name").text,
                    quantity=tag.find('span', 'footnote1-r').text,
                    price=tag.find('p', 'product-price__unit-price subhead1-b').text
                ))

            sleep(0.25)

pd.DataFrame(
    [[p.title, p.quantity, p.price] for p in list_products],
    columns=['title', 'quantity', 'price'],

).to_csv('products3.csv', sep=";")