from lxml import html, etree
import csv, os, json
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import timeit
import os.path

#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Product:
    
    all_data = []
    def __init__(self, url, related=True):
        print ("Processing: " + url)
        data = self.parse(url, related)

        self.name = data['NAME']
        self.name = unicode(self.name, errors='ignore')
        self.sale_price = data['SALE_PRICE']
        self.sale_str = "${:0.2f}".format(self.sale_price) if self.sale_price else "See Product Options For Sale Price"
        self.original_price = data['ORIGINAL_PRICE']
        self.original_price_str = "${:0.2f}".format(self.original_price) if self.original_price else "See Product Options For Original Price"
        self.category = data['CATEGORY']
        self.availability = data['AVAILABILITY']
        self.url = data['URL']
        self.related_links = data['RELATED_LINKS']

        for related_url in self.related_links[:5]:
            Product.all_data.append(Product("http://www.amazon.com/" + related_url, related=False))

    def __repr__(self):
        string = "Name: " + str(self.name) + "\n"
        string += "Sale Price: " + str(self.sale_price) + "\n"
        string += "Original Price: " + str(self.original_price) + "\n"
        string += "Category: " + str(self.category) + "\n"
        string += "Avaliability: " + str(self.availability) + "\n"
        string += "\n"

        return string

    def parse(self, url, related):
        path = "/home/akashv/Documents/phantomjs/bin/phantomjs"
        browser = webdriver.PhantomJS(path)
        browser.get(url)
        doc = html.fromstring(browser.page_source)
        browser.close()

        XPATH_NAME = '//h1[@id="title"]//text()'
        XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
        XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
        XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
        XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

        RAW_NAME = doc.xpath(XPATH_NAME)
        RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
        RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
        RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
        RAW_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)

        NAME = ' '.join(''.join(RAW_NAME).encode('utf-8').split()) if RAW_NAME else None
        SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
        if SALE_PRICE:    
            if "-" in SALE_PRICE:
                t = SALE_PRICE.index('-')
                SALE_PRICE = SALE_PRICE[:t]
            SALE_PRICE = eval(SALE_PRICE[1:])
        CATEGORY = ' > '.join([i.encode('utf-8').strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
        ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
        ORIGINAL_PRICE = eval(ORIGINAL_PRICE[1:]) if ORIGINAL_PRICE else None
        AVAILABILITY = ''.join(RAW_AVAILABILITY).strip() if RAW_AVAILABILITY else None
        if AVAILABILITY:
             AVAILABILITY = ' '.join(AVAILABILITY.split())

        RELATED_LINKS = []

        if related:
            RELATED_LINKS = self.related_links(doc)

        if not ORIGINAL_PRICE:
            ORIGINAL_PRICE = SALE_PRICE

        data = {
                'NAME': NAME,
                'SALE_PRICE': SALE_PRICE,
                'CATEGORY': CATEGORY,
                'ORIGINAL_PRICE': ORIGINAL_PRICE,
                'AVAILABILITY': AVAILABILITY,
                'URL': url,
                'RELATED_LINKS': RELATED_LINKS
                }
        return data

    def related_links(self, doc):
        #time.sleep(.5)
        div = doc.xpath('//*[@id="session-sims-feature" or @id="purchase-sims-feature" or @id="sponsoredProducts2_feature_div" or @id="zg_centerListWrapper"]/div')[0]
        related_links = [] 
        for li in div.xpath('*//ol/li'):
            related_links.append(li.xpath('*//a/@href')[0])
        return related_links

def ReadAsin(ASIN_list):
    product_list = []
    for ASIN in ASIN_list:
        url = "http://www.amazon.com/dp/" + ASIN
        product_list.append(Product(url))
    return product_list


def SearchList(textsearch, n):
    Product.all_data = []
    # path = "C:\Users\uditc\Desktop\scraper\cmpe130\chromedriver"
    path = "/home/akashv/Documents/phantomjs/bin/phantomjs"
    #path = r'C:\Users\uditc\Desktop\scraper\cmpe130\phantomjs-2.1.1-windows\bin\phantomjs'
    product_list = []

    # path = "/home/akashv/Documents/Selenium/chromedriver"
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    browser = webdriver.PhantomJS(path)
    browser.get("http://www.amazon.com/")
    search = browser.find_element_by_id("twotabsearchtextbox")
    search.send_keys(textsearch + u'\ue007')


    content = browser.page_source
    doc = html.fromstring(content)
    browser.close()

    URL = '//*[@id="s-results-list-atf"]/li'  

    ul = doc.xpath(URL)

    for li in ul[:n]:
        href = li.xpath('*//a/@href')[0]
        if "https://www.amazon.com" not in href:
            href = "https://www.amazon.com" + href
        product_list.append(Product(href))
    return product_list

def ascending_original(product1, product2):
    return product1.original_price < product2.original_price

def descending_original(product1, product2):
    return product1.original_price > product2.original_price

def mergeSort(ranking, alist):
    #print("Splitting ",alist)
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(ranking, lefthalf)
        mergeSort(ranking, righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            # lefthalf[i].ORIGINAL_PRICE < righthalf[j].ORIGINAL_PRICE
            if ranking(lefthalf[i], righthalf[j]):
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

    return alist

def file(product_list, similar_products):
    file_name = 'data.html'
    save_path = r'C:\Users\uditc\Desktop\scraper\cmpe130\webapp\templates'
    complete_name = os.path.join(save_path,file_name)

    file = open(complete_name,'w')

    count = 1
    file.write("<head>")
    file.write("<a href ='http://localhost:5000/#services'>Search For Another Product</a>")
    file.write("<style>")
    file.write("body {background-color: lightblue;}")
    file.write("</style></head>")
    file.write("<body>")
    file.write("<pre>")
    for product in product_list:
        file.write("Product " + str(count) + "\n") #Sorts and Displays Primary Search Page Products
        file.write(str(product))
        count += 1

    count = 1
    for product in similar_products:
        file.write("Related Product " + str(count) + "\n") #Sorts and Displays Related Products
        file.write(str(product))
        count += 1
    file.write("</pre></body>")
    file.close()

if __name__ == "__main__":
    start = timeit.default_timer()
    start_parse = timeit.default_timer()
    product_list = SearchList("iPhone", 3)
    stop_parse = timeit.default_timer() - start_parse

    file_name = 'data.html'
    save_path = r'C:\Users\uditc\Desktop\scraper\cmpe130\webapp\templates'
    complete_name = os.path.join(save_path,file_name)

    file = open(complete_name,'w')

    start_mergeA = timeit.default_timer()
    product_list = mergeSort(ascending_original, product_list)
    count = 1

    file.write("<pre>")
    for product in product_list:
        file.write("Product " + str(count) + "\n") #Sorts and Displays Primary Search Page Products
        file.write(str(product))
        count += 1
    stop_mergeA = timeit.default_timer() - start_mergeA
    start_mergeD = timeit.default_timer()
    Product.all_data = mergeSort(descending_original, Product.all_data)
    
    count = 1
    for product in Product.all_data:
        file.write("Related Product " + str(count) + "\n") #Sorts and Displays Related Products
        file.write(str(product))
        count += 1
    stop_mergeD = timeit.default_timer() - start_mergeD
    file.write("</pre>")
    file.close()
    stop = timeit.default_timer() - start
    product_list = []
    Product.all_data = []
    print "Parse time:", stop_parse
    print "Merge A Time:", stop_mergeA
    print "Merge D Time:", stop_mergeD
    print "Stop to Finish:", stop