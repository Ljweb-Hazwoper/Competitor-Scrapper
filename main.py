import os 
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
import re
import time
import boto3


df=pd.read_excel("competitor_price.xlsx")
print(df.head())
s3_client = boto3.client('s3',
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name=""
    )

bucket_name='qa-media.hazwoper-osha.com'
object_key='competitor_price/competitor_price.xlsx'
response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
data=response['Body'].read()
print(data)





service = Service()
options = webdriver.EdgeOptions()
options.set_capability("pageLoadStrategy", "normal")

def course_price_360training():
    driver = webdriver.Edge(options=options, service=service)
    for i in range(len(df)):
        if  pd.notna(df.loc[i,'360training_links']):
            
            driver.get(df['360training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "course-box__price")))
            price=driver.find_element(by=By.CLASS_NAME, value="course-box__price")
            
            if price.text.lower().__contains__('free'):
                df.loc[i,'360training_price']="0"
                print(0)
            else:    
                df.loc[i,'360training_price']=price.text.replace('$','')
                print("price",price.text)
    driver.close()

def price_osha_education_center():
    driver = webdriver.Edge(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'education_center_links']):
            driver.get(df['education_center_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "price")))
            price=driver.find_element(by=By.CLASS_NAME, value="price")
           
            if price.text.lower().__contains__('free'):
                df.loc[i,'OSHA Education Center']="0"
                print(0)
            else:    
                df.loc[i,'OSHA Education Center']=price.text.replace('$','')
                print(price.text)
    driver.close()            

def course_price_safety_limited():
    driver = webdriver.Edge(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'safety_limited_links']):
            driver.get(df['safety_limited_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[8]/div[2]/div[2]/div[1]/div[2]")))
            price=driver.find_element(by=By.XPATH,value="/html/body/div[8]/div[2]/div[2]/div[1]/div[2]/span/span")
            
            if price.text.lower().__contains__('free'):
                df.loc[i,'Safety Unlimited, Inc']="0"
                print(0)
            else:    
                df.loc[i,'Safety Unlimited, Inc']=price.text.replace('$','')
                print("price",price.text)

    driver.close()

def course_price_compliance_training():
    driver = webdriver.Edge(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'compliance_training_links']):
            driver.get(df['compliance_training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="formAddToCart"]/fieldset/div[1]/div[1]')))
            price=driver.find_element(by=By.XPATH, value='//*[@id="formAddToCart"]/fieldset/div[1]/div[1]')
            
            if price.text.lower().__contains__('free'):
                df.loc[i,'Compliance Training Online']="0"
                print(0)
            else:   
                price=re.search("\$?(\d+)\.?(\d+)",price.text).group().replace('$','')
                df.loc[i,'Compliance Training Online']=price
                print("price",price)

    driver.close()

def course_price_click_safety():

    driver = webdriver.Edge(service=service, options=options)
    price=""
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
                
              

            except:
                try:
                    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-info-price')))
                    price=driver.find_element(by=By.CLASS_NAME, value='product-info-price')
                   
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
    options = webdriver.EdgeOptions()
    options.set_capability("pageLoadStrategy", "eager")
    driver = webdriver.Edge(service=service, options=options)
    
    for i in range(len(df)):
        if pd.notna(df.loc[i,'hazmat_student_links']):
            driver.get(df['hazmat_student_links'][i])
            driver.find_element(by=By.TAG_NAME, value='html').send_keys(Keys.ESCAPE)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'breadcrumb_banner_price')))
            driver.execute_script("window.stop();")
            price_banner=driver.find_element(by=By.CLASS_NAME, value='breadcrumb_banner_price')
            price=price_banner.find_element(by=By.TAG_NAME, value='a')
            
            print("These are links",df['hazmat_student_links'][i])
            if price.text.lower().__contains__('free'):
                df.loc[i,'HAZMAT Student']="0"
                print(0)
            else:   
                price=re.search("\$?(\d+)\.?(\d+)",price.text).group().replace("$" , "")
                df.loc[i,'HAZMAT Student']=price
                print("price",price)
    driver.close()

def national_environment_price():
    driver = webdriver.Edge(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'national_environment_links']):
            driver.get(df['national_environment_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'course_detail_header')))
            course_header=driver.find_element(by=By.ID, value='course_detail_header')
            price=course_header.find_element(by=By.CLASS_NAME,value="course_price")
            
            if price.text.lower().__contains__('free'):
                df.loc[i,'National Environmental Trainers']="0"
                print(0)
            else:   
                price=re.search("\$?(\d+)\.?(\d+)",price.text).group().replace("$" , "")
                df.loc[i,'National Environmental Trainers']=price
                print("price",price)
    driver.close()

def lion_technology_price():
    driver = webdriver.Edge(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'lion_technology_links']):
            driver.get(df['lion_technology_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'detail-top')))
            detail_header=driver.find_element(by=By.CLASS_NAME, value='detail-top')
            price=detail_header.find_element(by=By.CLASS_NAME,value="priceRange")
            
            if price.text.lower().__contains__('free'):
                df.loc[i,'Lion Technology']="0"
                print(0)
            else:   
                price=re.search("\$?(\d+)\.?(\d+)",price.text).group().replace("$" , "")
                df.loc[i,'Lion Technology']=price
                print("price",price)
    driver.close()

def online_osha_training_price():
    driver = webdriver.Edge(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'online_osha_training_links']):
            driver.get(df['online_osha_training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'courseInfoBox')))
            price_container=driver.find_element(by=By.ID, value='courseInfoBox')
            price=price_container.find_element(by=By.CLASS_NAME,value="price-new")
            
            if price.text.lower().__contains__('free'):
                df.loc[i,'Online OSHA Training']="0"
                print(0)
            else:   
                
                price=re.search("\$?(\d+)\.?(\d+)",price.text).group().replace("$","")
                df.loc[i,'Online OSHA Training']=price
                print("Price ",price)
    driver.close()

def semi_course_price():
    driver = webdriver.Edge(service=service, options=options)
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
                price=re.search("\$?(\d+)\.?(\d+)",price.text).group().replace('$','')
                df.loc[i,'Semi']=price
                print("price",price)
    driver.close()

def osha_training_course_price():
    driver = webdriver.Edge(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'osha_training_links']):
            driver.get(df['osha_training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/main/article/div/div/section[4]/div/div/div/section/div[2]/div/div/div[1]/div/h2')))
            price=driver.find_element(by=By.XPATH,value='/html/body/div[1]/div[2]/div/div/main/article/div/div/section[4]/div/div/div/section/div[2]/div/div/div[1]/div/h2')
            
            if price.text.lower().__contains__('free'):
                df.loc[i,'OSHA Training']="0"
                print(0)
            else:   
                price=re.search("\$?(\d+)\.?(\d+)",price.text).group().replace('$','')  
                df.loc[i,'OSHA Training']=price
                print("price",price)

    driver.close()

def hazwoper_training_course_price():
    driver = webdriver.Edge(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'hazwoper_training_links']):
            driver.get(df['hazwoper_training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'sidebar')))
            price_container=driver.find_element(by=By.ID, value='sidebar')
            price=price_container.find_element(by=By.XPATH,value='//*[@id="sidebar"]/div/ul[3]/li[2]/p/span/strong')
            
            if price.text.lower().__contains__('free'):
                df.loc[i,'HAZWOPER Training']="0"
                print(0)
            else:   
                price=re.search("\$?(\d+)\.?(\d+)",price.text).group().replace("$",'')
                df.loc[i,'HAZWOPER Training']=price
                print("price",price)
    driver.close()

def hard_hat_course_price():
    driver = webdriver.Edge(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'hard_hat_links']):
            driver.get(df['hard_hat_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'summary')))
            price_container=driver.find_element(by=By.CLASS_NAME, value='summary')
            price=price_container.find_element(by=By.CLASS_NAME,value='price')
            
            if price.text.lower().__contains__('free'):
                df.loc[i,'Hard Hat']="0"
                print(0)
            else:   
                price=re.search("\$?(\d+)\.?(\d+)",price.text).group().replace('$','')
                df.loc[i,'Hard Hat']=price
                print("price",price)                
    driver.close()

def eduwhere_course_price():
    driver = webdriver.Edge(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'eduwhere_links']):
            driver.get(df['eduwhere_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'enroll-box')))
            price_container=driver.find_element(by=By.CLASS_NAME, value='enroll-box')
            price=price_container.find_element(by=By.CLASS_NAME,value='enroll-price-amount')
            
            if price.text.lower().__contains__('free'):
                df.loc[i,'Eduwhere']="0"
                print(0)
            else:   
                price=float(re.search("\$?(\d+)\.?(\d+)",price.text).group().replace('$',''))
                df.loc[i,'Eduwhere']=price
                print("price",price)                
    driver.close()


def dci_training_course_price():
    driver = webdriver.Edge(service=service, options=options)
    for i in range(len(df)):
        if pd.notna(df.loc[i,'dci_training_links']):
            driver.get(df['dci_training_links'][i])
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'productView-price')))
            price=driver.find_element(by=By.CLASS_NAME, value='productView-price')
            
            if price.text.lower().__contains__('free'):
                df.loc[i,'DCI Training Center']="0"
                print(0)
            else:   
                price=float(re.search("\$?(\d+)\.?(\d+)",price.text).group().replace('$',''))
                df.loc[i,'DCI Training Center']=price
                print("price",price)                
    driver.close()    


course_price_hazmat_student()
eduwhere_course_price()
time.sleep(2)
hard_hat_course_price()
time.sleep(2)
hazwoper_training_course_price()
time.sleep(2)
online_osha_training_price()
time.sleep(2)
lion_technology_price()
time.sleep(2)
course_price_click_safety()
time.sleep(2)
course_price_safety_limited()
time.sleep(2)
course_price_compliance_training()
time.sleep(2)
national_environment_price()
time.sleep(2)
course_price_360training()
time.sleep(2)
price_osha_education_center()
time.sleep(2)
semi_course_price()

df.to_excel("competitor_price.xlsx",index=False)


df=pd.read_excel("competitor_price.xlsx")
for col in df.columns:
    if col.__contains__("courses"):
        print(col)
        df.drop([col],axis=1, inplace=True)

df['360 Training']=df['360training_links']+'  '+df['360training_duration']+'  '+df['360training_price'].astype('str')
df['Safety Unlimited']=df['safety_limited_links']+'  '+df['safety_limited_duration']+'  '+df['Safety Unlimited, Inc'].astype('str')
df['Semi']=df['semi_links']+'  '+df['semi_duration']+'  '+df['Semi '].astype('str')
df['Online OSHA Training']=df['online_osha_training_links']+'  '+df['online_osha_training_duration']+'  '+df['Online OSHA Training'].astype('str')
df['OSHA Education Center']=df['education_center_links']+'  '+df['education_center_duration']+'  '+df['OSHA Education Center'].astype('str')
df['Compliance Training']=df['compliance_training_links']+'  '+df['compliance_training_duration']+'  '+df['Compliance Training Online'].astype('str')
df['DGI Training']=df['dci_training_links']+'  '+df['dci_training_duration']+'  '+df['DCI Training Center'].astype('str')
df['Hard Hat']=df['hard_hat_links']+'  '+df['hard_hat_duration']+'  '+df['Hard Hat'].astype('str')
df['Eduwhere']=df['eduwhere_links']+'  '+df['eduwhere_duration']+'  '+df['Eduwhere'].astype('str')
df['HAZMAT Student']=df['hazmat_student_links']+'  '+df['hazmat_student_duration']+'  '+df['HAZMAT Student'].astype("str")
df['Lion Technology']=df['lion_technology_links']+'  '+df['lion_technology_duration']+'  '+df['Lion Technology'].astype("str")
df['Click Safety']=df['click_safety_links']+'  '+df['click_safety_duration']+'  '+df['Click Safety'].astype("str")
df['National Environmental Trainer']=df['national_environment_links']+'  '+df['national_environment_duration']+'  '+df['National Environmental Trainers'].astype("str")
df['Hazwoper Hazmat']=df['hazwoper_training_links']+'  '+df['hazwoper_training_duration']+'  '+df['HAZWOPER Training'].astype('str')


for col in df.columns:
    if col.__contains__("duration") or col.__contains__("price") or col.__contains__("links"):
        df.drop([col],axis=1,inplace=True)

df.drop(['Safety Unlimited, Inc','Semi ','Hard Hat ','National Environmental Trainers','HAZWOPER Training','Compliance Training Online','Compliance Training Online ','DCI Training Center','Online OSHA Training ','OSHA Training'],axis=1,inplace=True)
df1=pd.melt(df,id_vars=['Courses','Duration','HAZWOPER OSHA Training'],var_name='Competitor',value_name='data')

df1['competitor_links']=df1['data'].apply(lambda x:str(x).split('  ')[0])
df1['competitor_duration']=df1['data'].apply(lambda x:str(x).split('  ')[1] if pd.notna(x) else np.nan)
df1['competitor_price']=df1['data'].apply(lambda x:float(str(x).split('  ')[2]) if pd.notna(x) else np.nan)

df1.to_excel("competitor_price_modified.xlsx")