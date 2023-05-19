import requests
import lxml
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv 

#############################LOAD PASSWORDS#######################
load_dotenv("C:/Users/Popuś/Desktop/Python/environment_variables/.env")

my_email= os.getenv("MY_EMAIL")
api_key_gmail = os.getenv("APP_PASSWORD_GMAIL")

BUY_PRICE = 200
################################BEAUTIFULSOUP######################################
URL = "https://www.amazon.com/Infant-Optics-Monitor-Screen-Resolution/dp/B08FF4GV5C/ref=sr_1_25?qid=1684498784&s=baby-products-intl-ship&sr=1-25" 
MY_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0"
MY_ACCEPT_LANG = "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"

web_headers = {
    "User-Agent": MY_USER_AGENT,
    "Accept-Language": MY_ACCEPT_LANG,
}
response = requests.get(URL, headers=web_headers)
page_lxml= response.text

soup = BeautifulSoup(page_lxml, "lxml")
# print(soup.prettify())
################################GET FINAL PRICE#############################################
web_price = soup.find(name="span", class_="a-offscreen")
# print(web_price)#<span class="a-offscreen">$199.99</span>
only_price = web_price.getText()
# print(only_price)#$199.99
split_price = only_price.split("$")
# print(split_price)#['', '199.99']
final_price = float(split_price[1])
print(final_price)

#############################GET NAME OF PRODUCT##########################################
product = soup.find(name="span", id="productTitle")
# print(amazon_product)#<span class="a-size-medium product-title-word-break product-title-resize" id="productTitle">Infant Optics DXR-8 PRO Video Baby Monitor</span>
title_product = product.getText()
amazon_product = title_product.strip()
print(amazon_product)


#############################SEND MAIL IF PRICE IS LOWER THAN BUY_PRICE#####################
if final_price <= BUY_PRICE:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=api_key_gmail)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f"Subject: Amazon Pice Change Alert\n\n A price for {amazon_product} is lower that you want {BUY_PRICE}$. It cost {final_price}$\n {URL}".encode("utf-8"))


