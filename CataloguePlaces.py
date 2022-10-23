import requests 
import re 
import json
import math 

from multiprocessing import Pool,\
        Manager

from functools import partial

# precompiled regex start 
find_data_urls = re.compile(r'''\"reviewUrl\":\[{\"url\":\"([^"]*)\"}]}''')
items_count = re.compile('''"initialDescHeader":"u003cspan class='highlight'>([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))? propertiesu003c/span>''')

def get_items_count(url1): 
    session = requests.Session()
    
    headers = {
        'authority': 'www.tripadvisor.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-device-memory': '4',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '".Not/A)Brand";v="99.0.0.0", "Google Chrome";v="103.0.5060.53", "Chromium";v="103.0.5060.53"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    response = session.get(url1, headers=headers)
    response_html = response.text.replace('\\', '')
    print(response_html)
    items_number = items_count.findall(response_html)
    return int(items_number[0][0])

def generate_pages_urls(url1, num): 
    num = num / 30 
    num = math.ceil(num)
    out = [] 
    for i in range(num): 
        out.append(url1.replace('.html', f'-oa{i*30}.html')) 
    return out

def get_items_out_of_page(url): 
    session = requests.Session()                                                                                                                                                                                                 
    headers = {                                                                                                                                                                                                                  
        'authority': 'www.tripadvisor.com',                                                                                                                                                                                      
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',                                                                     
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',                                                                                                                                                                
        'cache-control': 'max-age=0',                                                                                                                                                                                            
        'sec-ch-device-memory': '4',                                                                                                                                                                                             
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',                                                                                                                                       
        'sec-ch-ua-arch': '"x86"',                                                                                                                                                                                               
        'sec-ch-ua-full-version-list': '".Not/A)Brand";v="99.0.0.0", "Google Chrome";v="103.0.5060.53", "Chromium";v="103.0.5060.53"',                                                                                           
        'sec-ch-ua-mobile': '?0',                                                                                                                                                                                                
        'sec-ch-ua-model': '""',                                                                                                                                                                                                 
        'sec-ch-ua-platform': '"Linux"',                                                                                                                                                                                         
        'sec-fetch-dest': 'document',                                                                                                                                                                                            
        'sec-fetch-mode': 'navigate',                                                                                                                                                                                            
        'sec-fetch-site': 'same-origin',                                                                                                                                                                                         
        'sec-fetch-user': '?1',                                                                                                                                                                                                  
        'upgrade-insecure-requests': '1',                                                                                                                                                                                        
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',                                                                                                   
    }                                                                                                                                                                                                                            
                                                                                                                                                                                                                                 
    response = session.get(url, headers=headers)                                                                                                                                                                                
    response_html = response.text.replace('\\', '')                                                                                                                                                                              
    items_urls = find_data_urls.findall(response_html)                 
    return items_urls

number_of_items = get_items_count('https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html')
pages_urls = generate_pages_urls('https://www.tripadvisor.com/Hotels-g60763-New_York_City_New_York-Hotels.html', number_of_items)

output = []

for i in pages_urls: 
    collected_data = get_items_out_of_page(i) 
    for d in list(set(collected_data)): 
        output.append(d) 

print(output)
print(len(output))
