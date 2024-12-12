from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service) 


driver.get("https://unstop.com/hackathons?oppstatus=open&domain=2&course=6&specialization=Computer%20Science&usertype=students&passingOutYear=2026&searchTerm=")


event_data = [] 

try:
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ng-star-inserted"))
    )

   
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
      
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        
        time.sleep(2) 

        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
         
            break
        last_height = new_height


    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "user_list"))
    )

 
    containers = driver.find_elements(By.CLASS_NAME, "user_list")
    
   
    for container in containers:
       
        events = container.find_elements(By.CLASS_NAME, "opp_content")
        
      
        for event in events:
            
            name = event.find_element(By.TAG_NAME, "h2").text
            
           
            organizer = event.find_element(By.TAG_NAME, "p").text
            
         
            try:
                prize = event.find_element(By.CLASS_NAME, "prize").text
            except:
                prize = "N/A"
            
          
           
            categories = []
            category_elements = event.find_elements(By.CLASS_NAME, "chip_text")
            for cat in category_elements:
                categories.append(cat.text)
            
           
            event_data.append({
                "Event Name": name,
                "Organizer": organizer,
                "Prize": prize,
                "Categories": ", ".join(categories),
            })

finally:
    
    driver.quit()


df = pd.DataFrame(event_data)
df.to_excel("event_data.xlsx", index=False)
print("Data has been saved to event_data.xlsx")