from playwright.async_api import async_playwright
import asyncio
import re
import pandas as pd
# from parsing_tools import BeautifulSoup
# from parsing_tools import ParsingTools
from urllib.request import urlopen
from bs4 import BeautifulSoup

All_data = []


def extract_data(All_data):
    for i in All_data:
        hotel_names = i.find('div', class_='_4rR01T').text
        print(hotel_names,"=========")
        Bank = re.findall('projectTable_bankBean.bankName"[^\"]+"[^=]+=[^=]+=.([^"]+)', str(i))
        Branch = re.findall('aria-describedby[^"]+"projectTable_branchBean.branchName[^=]+=[^=]+=[^=]+="([^"]+)"',
                            str(i))
        Quater = re.findall('projectTable_quarterBean.quarterDateStr"[^"]+"[^=]+=[^=]+=.([^"]+)', str(i))
        Address = re.findall('projectTable_importDataBean.regaddr"[^"]+"[^=]+=[^=]+=.([^"]+)', str(i))
        Direct_name = re.findall('projectTable_directorName"[^"]+"[^=]+=[^=]+=.([^"]+)', str(i))
        Amount = re.findall('projectTable_totalAmount"[^"]+"[^=]+=[^=]+=.([^"]+)', str(i))
        Borrowser_name = re.findall('projectTable_borrowerName"[^"]+"[^=]+=[^=]+=.([^"]+)', str(i))

        df = pd.DataFrame(
            {'Bank': Bank, 'Branch': Branch, 'Quater': Quater, 'Borrowser_name': Borrowser_name, 'Address': Address,
             'Direct_name': Direct_name, 'Amount': Amount})
        # print(df)
        df.to_csv('file1.csv')

        # print(Bank)

        # print('           ')
        # print(Branch)
        # print('           ')
        # print(Quater)
        # print('           ')
        # print(Borrowser_name)
        # print('           ')
        # print(Address)
        # print('           ')
        # print(Direct_name)
        # print('           ')
        # print(Amount)


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=False  # Show the browser
        )
        page = await browser.new_page()
        await page.goto('https://www.spicejet.com/')
        # Data Extraction Code Here
        await page.wait_for_timeout(2000)  # Wait for 1 second
        await page.click("//*[@clASS='css-76zvg2 r-homxoj r-ubezar r-1ozqkpa' and text() ='one way']")
        await page.wait_for_timeout(2000)
        #await page.keyboard.press("ArrowDown")
        await page.click('(//*[@class="css-1cwyjr8 r-homxoj r-ubezar r-10paoce r-13qz1uu"])[1]')

        #await page.wait_for_timeout(2000)
        #await page.keyboard.press("Enter")
        # await page.click('//select[@id = "croreAccount"]//option[text() = "Search"]')
        #await page.wait_for_timeout(2000)
        #await page.click('(//div[@class = "sfc-search-arrow"]/img)[3]')
        #await page.wait_for_timeout(2000)
        await page.click("//*[@class='css-76zvg2 r-cqee49 r-ubezar r-1kfrs79'  and text()='Mumbai']")
        await page.wait_for_timeout(2000)
        await page.keyboard.type('Delhi', delay=100)
        await page.keyboard.press("Enter")
        #await page.click('(//div[@class = "custombutton"]/input)[1]')
        await page.wait_for_timeout(30000)
        print("enter step1")
        await page.click("//*[@class='css-1dbjc4n r-1awozwy r-z2wwpe r-1loqt21 r-18u37iz r-1777fci r-1g94qm0 r-1w50u8q r-ah5dr5 r-1otgn73'] ")
        #for i in range(1, 2):
        html_data = await page.content()
            #await page.evaluate('window.scrollBy(0,900)')
        soup = BeautifulSoup(html_data, "html5lib")
        print(soup)
        list_div = soup.findAll('div', class_='css-1dbjc4n r-14lw9ot r-3aj1re r-18u37iz')
        print(list_div,"---------------------")
        await page.wait_for_timeout(30000)
        All_data.append(list_div)
            # print(All_data)
            # await page.click('//td[@id = "next_pagingDiv"]')
            # await page.wait_for_timeout(40000)
            # print(i)
        # await page.evaluate('window.scrollBy(0,500)')
        # print(All_data)
        print(len(All_data))
        extract_data(All_data)
        print(All_data,"--------------")
        await page.wait_for_timeout(6000)
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())