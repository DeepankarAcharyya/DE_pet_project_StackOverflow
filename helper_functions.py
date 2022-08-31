import os
import datetime
import csv
import time
import requests

def write_to_csv(dict_data_list, outputfile, pageNumber):
    columns = list(dict_data_list[0].keys())
    try:
        with open(outputfile, 'w',newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            if pageNumber==1:
                writer.writeheader()
            for eachrow in dict_data_list:
                writer.writerow(eachrow)
    except IOError:
        print("I/O error encountered")
   

#the data download function : the function downloads the data from the 
def scrape_data(section, fromdate):
    base_url = "https://api.stackexchange.com/2.3/{section_name}?page={page_count}&pagesize={pagesize_thres}&fromdate={start_date}&todate={end_date}&order=desc&sort=activity&site=stackoverflow"
    pageCount = 0
    pagesize = 20
    
    todate =  fromdate + datetime.timedelta(days=1)
    fromdate = int(fromdate.timestamp())
    todate = int(todate.timestamp())
    
    backoff = 0
    scrapeFlag = True

    csv_output = os.path.join(os.getcwd() , str(fromdate)+'.csv')
    
    while scrapeFlag :
        pageCount = pageCount + 1
        url = base_url.format(section_name=section, page_count = pageCount, pagesize_thres=pagesize,start_date=fromdate,end_date=todate)
        try:
            response = requests.get(url)
            content = response.json()
            
            result_items = content['items']
            write_to_csv(result_items, csv_output, pageCount)

            scrapeFlag = content['has_more']
            
            if 'backoff' in content.keys():
                backoff = content['backoff']
            
            if backoff > 0 :
                time.sleep(backoff)
        
        except Exception as e:
            print('Error encountered : ',e)

    return csv_output