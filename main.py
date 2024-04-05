from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
import re


df=pd.read_excel("competitor_price.xlsx")
print(df.head())

service = Service()
options = webdriver.ChromeOptions()

def course_price_360training():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if  pd.notna(df.loc[i,'360training_links']):
            print("These are links", df['360training_links'][i])
            driver.get(df['360training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "course-box__price")))
            price=driver.find_element(by=By.CLASS_NAME, value="course-box__price")
            print("These are links", df['360training_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'360training_price']="0"
                print(0)
            else:    
                df.loc[i,'360training_price']=price.text.replace('$','')
                print(price.text)
    driver.close()

def price_osha_education_center():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'education_center_links']):
            driver.get(df['education_center_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "price")))
            price=driver.find_element(by=By.CLASS_NAME, value="price")
            print("These are links",df['education_center_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'OSHA Education Center']="0"
                print(0)
            else:    
                df.loc[i,'OSHA Education Center']=price.text.replace('$','')
                print(price.text)
    driver.close()            

def course_price_safety_limited():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'safety_limited_links']):
            driver.get(df['safety_limited_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div[2]/div[2]/div[1]/div[2]/span/span")))
            price=driver.find_element(by=By.XPATH, value="/html/body/div[8]/div[2]/div[2]/div[1]/div[2]/span/span")
            print("These are links",df['safety_limited_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'Safety Unlimited, Inc']="0"
                print(0)
            else:    
                df.loc[i,'Safety Unlimited, Inc']=price.text.replace('$','')
                print(price.text)

    driver.close()

def course_price_compliance_training():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'compliance_training_links']):
            driver.get(df['compliance_training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="formAddToCart"]/fieldset/div[1]/div[1]')))
            price=driver.find_element(by=By.XPATH, value='//*[@id="formAddToCart"]/fieldset/div[1]/div[1]')
            print("These are links",df['compliance_training_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'Compliance Training Online']="0"
                print(0)
            else:   
                price=re.search("\$[0-9]*?\.[0-9]*",price.text).group().replace('$','')
                df.loc[i,'Compliance Training Online']=price
                print("price",price)

    driver.close()

def course_price_click_safety():

    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'click_safety_links']):
            driver.get(df['click_safety_links'][i])
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-options-wrapper')))
                product_options=driver.find_element(by=By.CLASS_NAME, value='product-options-wrapper')
                control=product_options.find_element(by=By.CLASS_NAME, value="control")
                selected_value=Select(control.find_element(by=By.TAG_NAME, value="select"))
                ActionChains(driver).click(control).perform()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="attribute716"]/option[2]')))
                items=control.find_element(by=By.CLASS_NAME,value='select-items')
                span_tags=items.find_elements(by=By.TAG_NAME,value="span")
                ActionChains(driver).click(span_tags[5]).perform()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-info-price')))
                price=driver.find_element(by=By.CLASS_NAME,value="product-info-price")
                print(df['click_safety_links'][i])
                print(price.text)

            except:
                try:
                    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-info-price')))
                    price=driver.find_element(by=By.CLASS_NAME, value='product-info-price')
                    print("These are links in except block",df['click_safety_links'][i])
                    print("These are price in except block",price.text)
                except:
                    print("Element not found")


            if price.text.lower().__contains__('free'):
                df.loc[i,'Click Safety']="0"
                print(0)
            else:   
                price=price.text.replace('$','')
                df.loc[i,'Click Safety']=price
                print("price",price)
    driver.close()

def course_price_hazmat_student():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'hazmat_student_links']):
            driver.get(df['hazmat_student_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'breadcrumb_banner_price')))
            price_banner=driver.find_element(by=By.CLASS_NAME, value='breadcrumb_banner_price')
            price=price_banner.find_element(by=By.TAG_NAME, value='a')
            print("These are links",df['hazmat_student_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'HAZMAT Student']="0"
                print(0)
            else:   
                price=re.search("\$[0-9]*?\.[0-9]*",price.text).group().replace("$" , "")
                df.loc[i,'HAZMAT Student']=price
                print("price",price)
    driver.close()

def national_environment_price():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'national_environment_links']):
            driver.get(df['national_environment_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'course_detail_header')))
            course_header=driver.find_element(by=By.ID, value='course_detail_header')
            price=course_header.find_element(by=By.CLASS_NAME,value="course_price")
            print("These are links",df['national_environment_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'National Environmental Trainers']="0"
                print(0)
            else:   
                price=re.search("\$[0-9]*?\.[0-9]*",price.text).group().replace("$" , "")
                df.loc[i,'National Environmental Trainers']=price
                print("price",price)
    driver.close()

def lion_technology_price():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'lion_technology_links']):
            driver.get(df['lion_technology_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'detail-top')))
            detail_header=driver.find_element(by=By.CLASS_NAME, value='detail-top')
            price=detail_header.find_element(by=By.CLASS_NAME,value="priceRange")
            print("These are links",df['lion_technology_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'Lion Technology']="0"
                print(0)
            else:   
                price=re.search("\$[0-9]*?\.[0-9]*",price.text).group().replace("$" , "")
                df.loc[i,'Lion Technology']=price
                print("price",price)
    driver.close()

def online_osha_training_price():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'online_osha_training_links']):
            driver.get(df['online_osha_training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'price-container')))
            price_container=driver.find_element(by=By.CLASS_NAME, value='price-container')
            price=price_container.find_element(by=By.CLASS_NAME,value="price-new")
            print("These are links",df['online_osha_training_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'Online OSHA Training']="0"
                print(0)
            else:   
                price=re.search("[0-9]*?\.[0-9]*",price.text).group()
                df.loc[i,'Online OSHA Training']=price
                print("price",price)
    driver.close()

def semi_course_price():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'semi_links']):
            driver.get(df['semi_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'price_bottom')))
            price_container=driver.find_element(by=By.CLASS_NAME, value='price_bottom')
            price=price_container.find_element(by=By.CLASS_NAME,value="price_amount_nonmember")
            print("These are links",df['semi_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'Semi']="0"
                print(0)
            else:   
                price=re.search("\$[0-9]*?\.[0-9]*",price.text).group().replace('$','')
                df.loc[i,'Semi']=price
                print("price",price)
    driver.close()

def osha_training_course_price():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'osha_training_links']):
            driver.get(df['osha_training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/main/article/div/div/section[4]/div/div/div/section/div[2]/div/div/div[1]/div/h2')))
            price=driver.find_element(by=By.XPATH,value='/html/body/div[1]/div[2]/div/div/main/article/div/div/section[4]/div/div/div/section/div[2]/div/div/div[1]/div/h2')
            print("These are links",df['osha_training_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'OSHA Training']="0"
                print(0)
            else:   
                price=re.search("\$[0-9]*?\.[0-9]*",price.text).group().replace('$','')  
                df.loc[i,'OSHA Training']=price
                print("price",price)

    driver.close()

def hazwoper_training_course_price():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'hazwoper_training_links']):
            driver.get(df['hazwoper_training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'sidebar')))
            price_container=driver.find_element(by=By.ID, value='sidebar')
            price=price_container.find_element(by=By.XPATH,value='//*[@id="sidebar"]/div/ul[3]/li[2]/p/span/strong')
            print("These are links",df['hazwoper_training_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'HAZWOPER Training']="0"
                print(0)
            else:   
                price=re.search("\$[0-9]*?\.[0-9]*",price.text).group().replace("$",'')
                df.loc[i,'HAZWOPER Training']=price
                print("price",price)
    driver.close()

def hard_hat_course_price():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'hard_hat_links']):
            driver.get(df['hard_hat_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'summary')))
            price_container=driver.find_element(by=By.CLASS_NAME, value='summary')
            price=price_container.find_element(by=By.CLASS_NAME,value='price')
            print("These are links",df['hard_hat_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'Hard Hat']="0"
                print(0)
            else:   
                price=re.search("\$[0-9]*?\.[0-9]*",price.text).group().replace('$','')
                df.loc[i,'Hard Hat']=price
                print("price",price)                
    driver.close()

def eduwhere_course_price():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'eduwhere_links']):
            driver.get(df['eduwhere_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'enroll-box')))
            price_container=driver.find_element(by=By.CLASS_NAME, value='enroll-box')
            price=price_container.find_element(by=By.CLASS_NAME,value='enroll-price-amount')
            print("These are links",df['eduwhere_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'Eduwhere']="0"
                print(0)
            else:   
                price=float(re.search("\$[0-9]*?\.[0-9]*",price.text).group().replace('$',''))
                df.loc[i,'Eduwhere']=price
                print("price",price)                
    driver.close()


def dci_training_course_price():
    driver = webdriver.Chrome(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'dci_training_links']):
            driver.get(df['dci_training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'productView-price')))
            price=driver.find_element(by=By.CLASS_NAME, value='productView-price')
            print("These are links",df['dci_training_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'DCI Training Center']="0"
                print(0)
            else:   
                price=float(re.search("\$[0-9]*?\.[0-9]*",price.text).group().replace('$',''))
                df.loc[i,'DCI Training Center']=price
                print("price",price)                
    driver.close()    


course_price_hazmat_student()

# course_price_compliance_training()
#dci_training_course_price()
# eduwhere_course_price()
# hard_hat_course_price()
# hazwoper_training_course_price()
# osha_training_course_price()
# semi_course_price()
# online_osha_training_price()
# lion_technology_price()
# course_price_click_safety()
#course_price_safety_limited()
#price_compliance_training()
#course_price_360training()
#price_osha_education_center()


# df.to_excel("competitor_price.xlsx",index=False)
