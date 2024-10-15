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

#Code without using threads
'''driver = webdriver.Chrome()
company_data=[]
for page in range(1,10):
    driver.get(f"https://www.zaubacorp.com/company-list/p-{page}-company.html")
    #time.sleep(1) #wait for page to load completly
    table=driver.find_element(By.ID,"table")
    rows = table.find_elements(By.XPATH, './/tbody/tr')

    for row in rows:
        cells=row.find_elements(By.TAG_NAME,'td')
        cin=cells[0].text
        company_name=cells[1].text  
        RoC=cells[2].text
        status=cells[3].text
        company_data.append([cin,company_name,RoC,status])

df=pd.DataFrame(company_data,columns=['Cin','Company Name','RoC','Status'])
df.to_csv('company_data.csv',index=False)       
driver.close() '''


'''import requests
from bs4 import BeautifulSoup
# URL of the webpage containing the table
url ='https://www.zaubacorp.com/company-list'
# Fetch the content of the webpage
headers={
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cookie':'_ga=GA1.2.1912691005.1710438866; __stripe_mid=4211ba2e-1435-433b-98e6-2688cd3201aa3d48fe; cf_clearance=qH6GDm6EpjP1l7JA7OxRJ5BD7p9dTLt75o.SHJywoVY-1710438868-1.0.1.1-5cxtbqMBif2HqdP89bFL7mL.H_wzOhxDybMZqiD7Wzu23rcr0fh9pR5Tx.pvWwOfDJ7eYqApsLqh6TuBr1gFpw; _gid=GA1.2.929487005.1720373066; __stripe_sid=913eb931-021e-445a-9a01-eb18e6b91e0ad47d1a; SSESSce35b9c5c670c92e0736ae2e23dbc9ab=XxdVC1f6-HMdCx36K6N3i_U5pK2w2gJ419q6iUZJkYk; _ga_VVR3BV80B8=GS1.2.1720373066.11.1.1720374727.41.0.0; __gads=ID=afbf1f11e5f39032:T=1710438866:RT=1720374727:S=ALNI_MbFqgLLAdwQI0vbWogvEsklRt8Spg; __gpi=UID=00000d37b185a2cc:T=1710438866:RT=1720374727:S=ALNI_MY9ut-0vDj5DyqqRrxBDimGbiRyFA; __eoi=ID=9de5369952e67dd3:T=1710438866:RT=1720374727:S=AA-AfjZ1I4pIDghTic3V7ZXHYzkj; FCNEC=%5B%5B%22AKsRol8WQqQ1zEQx4PEJn70Iomx-eczpTPm_Rh8K14W-gLgLe_xxOVy3H3JiyTnzrTCaKxo2UqCTpY9HjUU3ngzlNH3DE64zYCMG-ohNFOx2uwctUX7TRR64NWbiHcnbol27HaZgPXFBDlBsCyf1qQqFKsPa5DmQZg%3D%3D%22%5D%5D',
    'Referer': 'https://www.zaubacorp.com/',
}
page = requests.get(url,headers=headers)
soup=BeautifulSoup(page.content,'html.parser')
tables=soup.find_all('table')
print(page.status_code)
tables=soup.find_all('table',{'class':'table table-striped col-md-12 col-sm-12 col-xs-12'})
if tables:
    company_names=[]
    for row in tables.find('tbody').find_all('tr'):
        company_name=row.find_all('td')[1].text.strip()
        company_names.append(company_name)
    for name in company_names:
        print(name)'''
