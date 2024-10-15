import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import threading
from queue import Queue

#Code with using threads
#function that run for each thread simultaneously
def scrap_pages(start_page,end_page,result_queue):  
    driver = webdriver.Chrome()
    company_data=[]
    for page in range(start_page,end_page):
        driver.get(f"https://www.zaubacorp.com/company-list/p-{page}-company.html")
        #time.sleep(1) #wait for page to load completely
        table=driver.find_element(By.ID,"table")
        rows = table.find_elements(By.XPATH, './/tbody/tr')

        for row in rows: #traverse the all rows for a single page
            cells=row.find_elements(By.TAG_NAME,'td') 
            cin=cells[0].text
            company_name=cells[1].text  
            RoC=cells[2].text
            status=cells[3].text
            company_data.append([cin,company_name,RoC,status]) #append the data for each company in company_data list    
    driver.close()
    result_queue.put(company_data)

num_threads=16  #using 16 threads
pages_per_thread=833 #each thread will work on 833(total pages are 13,333 so 13333/16=833)pages,but last thread would work on 5 extra pages
thread_list=[]
result_queue=Queue()

for i in range (num_threads): #traverse for all threads
    start_page=i*pages_per_thread+1
    end_page=start_page + pages_per_thread
    if(i==num_threads-1): #last thread would have all the left over pages
        end_page=13334
    
    #initialise the thread object
    t=threading.Thread(target=scrap_pages, args=(start_page,end_page,result_queue))
    thread_list.append(t)
    t.start() #return immediately after starting the thread

for thread in thread_list: #waiting for all theread to complete its execution
    thread.join() #it block the main program until current thread execution is completed

company_data=[]
while not result_queue.empty():
    #Queue.get() also remove the item from the queue, so while loop would not be infinite
    company_data.extend(result_queue.get()) 

df=pd.DataFrame(company_data,columns=['Cin','Company Name','RoC','Status'])
df.to_csv('company_data.csv',index=False) 


