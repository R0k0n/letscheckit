from cgi import print_environ
from unittest import result
from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio

async def get_page(session , url):
    async with session.get(url) as r:
        return await r.text()
    
async def get_all(session , urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session , url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await get_all(session , urls)
        return data
                 

def parse(scraper):
    acs = 0
    was = 0
    for html in scraper:
        soup = BeautifulSoup(html , "html.parser") 
        acob = soup.find_all('span' , class_ = 'verdict-accepted')
        waob = soup.find_all('span' , class_ = 'verdict-rejected')              
        acs = acs + len(acob)
        was = was + len(waob)
    return [acs , was]

def mx_page(url):
    pg_sub1 = requests.get(url)
    soup = BeautifulSoup(pg_sub1.content , 'html.parser')
    pg_no = soup.find_all('span' , class_ = 'page-index')
    mx = 1
    for x in pg_no:
       num = int(x.text)
       mx = max(num , mx)
    return mx



lnk = "https://codeforces.com/submissions/_SHADOW"
    
mx = mx_page(lnk)

urls = []

acs = 0
was = 0

for x in range(1 , mx + 1):
    new_url = lnk + "/page/" + str(x)
    urls.append(new_url)
    
results = asyncio.run(main(urls))
ans = parse(results)
print(ans)
