import asyncio
import aiohttp  # pip install aiohttp aiodns
import time
from bs4 import BeautifulSoup
import urllib.request, requests
from random import randrange
import time
i=0
#api_key = "YOUR TG API KEY HERE"
#chat_id = "YOUR TG CHAT ID HERE"
rand=randrange(904625697166532776746648320380374280100293470930272690489102837043110636675)
async def get(
    session: aiohttp.ClientSession,
    address: str,

    **kwargs
) -> dict:
    global i
    url = f"https://explorer.digiassets.net/api/addr/{address}/balance"
    try:
        resp = await session.request('GET', url=url, **kwargs)
        data = await resp.json(content_type=None)
        bal = int(data)
        i += 1
        if bal > 0:
            loot = f"Collision found at address: {address}\nPage no. :{rand}\n"
            print (loot)
            print ("Writing to loot.txt...")
            lootxt = open("loot.txt", 'a')
            lootxt.write(loot)
            lootxt.close()
            # Uncomment the below lines to send the loot to your telegram bot
            # s = loot.replace(" ", "%20")
            # urltg = "https://api.telegram.org/bot"+ api_key + "/sendMessage?chat_id=" + chat_id + "&text="
            # msg = urltg + s
            # ret = requests.get(msg)
        time.sleep(5)
        return data
    except asyncio.TimeoutError:
            pass
    except Exception as e:
            print("Error: "+repr(e))
            time.sleep(5)


async def main(addresses, **kwargs):
    global i
    async with aiohttp.ClientSession() as session:
        htmls = await asyncio.gather(*[get(session, addr, **kwargs) for addr in addresses])
        return htmls

if __name__ == '__main__':
    n=0
    while True:
        addresses = []
        try:          
            URL = 'https://lbc.cryptoguru.org/dio/'+str(rand)
            page = requests.get(URL)
            priv=[]
            pub=[]
            pub2=[]
            print("Page no. :",rand)
            print("\n\n--------------------------------------------\n\n")
            soup = BeautifulSoup(page.content, 'html.parser')
            for each_span in soup.findAll('span'):
                address=each_span.text
                row=address.split()
                if n%2==0:
                    priv.append(row[1])
                    pub.append(row[2])
                    pub2.append(row[3])
                n+=1
            for item in pub:
                addresses.append(item)
            for item in pub2:
                addresses.append(item)
            rand+=1
        except Exception as e:
            print("Error: "+repr(e))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(addresses))
