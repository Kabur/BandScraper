import random
from time import sleep
import sys
import bs4 as bs
import requests
import urllib.parse
import urllib.request
import re

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<tag1>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.
</p>
</tag1>

<p class="story">...</p>
</body>
</html>
"""
# test_soup = bs.BeautifulSoup(html_doc, 'lxml')
# print(test_soup.find('body').contents)
# exit()

# print(soup.find_all('a', id='link2'))
# print(soup.find_all(href=re.compile("example"), limit=1))
# print(soup.find_all(string=re.compile("sisters")))

# url = 'https://en.wikipedia.org/wiki/Leprous'
# ayreon, leprous, the algorithm
# headers = {
#     'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
# req = urllib.request.Request(url, headers=headers)
# source = urllib.request.urlopen(req)
# soup = bs.BeautifulSoup(source, 'lxml')
def find_album_table(sibling):
    while sibling is not None:
        # its a subheader like "Live Albums" - skip two times or skip once and break
        if sibling.name == "h3":
            text = sibling.find('span').get_text().lower()
            if ("albums" not in text and band not in text) or "live" in text:
                sibling = sibling.find_next_sibling()
            else:
                band_dict['band'] = band_dict['band'] + ' ' + text
                sibling = sibling.find_next_sibling()
                return sibling
        # There was no more junk or subheaders
        elif sibling.name == 'ul':
            return sibling
        elif sibling.name == 'div':
            inside_div = find_album_table(sibling.contents[0])
            if inside_div is not None:
                return inside_div
        sibling = sibling.find_next_sibling()

    return sibling


def find_wiki_link(string):
    query = "site:en.wikipedia.org+" + string
    query = query.replace(" ", "+")
    response = requests.get("https://www.google.com/search?q=" + query)
    soup = bs.BeautifulSoup(response.text, "lxml")

    link = soup.find('h3', attrs={'class': 'r'}) # Guides BS to h3 class "r" where green Wikipedia URLs are located, then prints URLs

    link = link.find("a").get("href")
    link = link[7:].split("&")[0] # [7:] strips the /url?q= prefix, split removes garbage in link after &

    return link

with open("all_bands_withlinks.txt", 'r') as file:
    bands = file.readlines()
    links = []

for i, band in enumerate(bands):
    links.append(band.split(',')[1][:-1])
    bands[i] = band.split(',')[0].lower()

# albums = []
dictionaries = []
for i, band in enumerate(bands):
    if band != 'periphery':
        continue
    # fix_list = [26, 38, 40, 45, 48, 50, 51, 53, 59, 61, 62, 66, 67, 68, 70, 71, 72, 74, 77, 79, 82, 83, 84, 88, 89]
    # skip = True
    # for item in fix_list:
    #     if i == item:
    #         skip = False
    #         break
    # if skip:
    #     continue
    try:

        band_dict = {'band': band}
        # link = find_wiki_link(band + ' band')
        link = links[i]
        response = requests.get(link)
        soup = bs.BeautifulSoup(response.content, 'lxml')

        # ''' find discography element '''
        discography = soup.find(id='Discography')
        disco_parent = discography.find_parent()

        # ''' Go sideways to find the table with albums '''
        album_table = find_album_table(disco_parent.find_next_sibling())

        ''' 
        Type 1:
        Table is present 
        '''
        if album_table.name == "table":
            table_rows = album_table.contents
            # table_rows = album_table.find_all('tr')
            #
            # row1 = table_rows[0].contents[1].get_text().lower()

            # in case there is a junk table row -> cut it
            i_tag = table_rows[-2].find('i')
            if i_tag is None:
                table_rows = table_rows[:-2]
                i_tag = table_rows[-2].find('i')

            # th = table_rows[-2].find('th')
            column1 = i_tag.parent  # todo: this is kinda lame.
            # test = album_table.find_all('tr')
            # print(test)
            # exit()
            # if its in <a>
            if i_tag.find("a") is not None:
                band_dict['album1'] = i_tag.find("a").get('title')
                # if its just in <i>
            else:
                band_dict['album1'] = i_tag.get_text()
            # td = th.find_next_sibling()
            column2 = column1.find_next_sibling()
            band_dict['year1'] = re.findall('\d{4}', column2.get_text())[0]

            # ''' same shit for the second album, should put it to a function prolly xD '''
            try:
                i_tag = table_rows[-4].find('i')
                column1 = i_tag.parent
                # th = table_rows[-4].find('th')
                # if its in <a>
                if i_tag.find("a") is not None:
                    band_dict['album2'] = i_tag.find("a").get('title')
                    # if its just in <i>
                else:
                    band_dict['album2'] = i_tag.get_text()

                column2 = column1.find_next_sibling()
                band_dict['year2'] = re.findall('\d{4}', column2.get_text())[0]
            except IndexError as e:
                band_dict['year2'] = 'NONE'
                band_dict['album2'] = 'NONE'
                print(str(e))

            ''' 
            TYPE 2:
            No table, just <ul> and <li> tags
            '''
        else:
            # sibling = disco_parent.find_next_sibling()

            # ''' Go sideways to find uls '''
            while album_table is not None and album_table.name != "ul":
                album_table = album_table.find_next_sibling()
            if album_table is None:
                print("DIDNT FIND AN ALBUM, INSPECT WIKI")
            else:
                lis = album_table.contents

                # sometimes there is a junk tag instead of the year -> cut
                if len(lis[-2].contents) > 1:
                    if re.match('.*\d{4}.*', str(lis[-2].contents[1])) is None:
                        del lis[-2].contents[1]
                        print("deleting junk line...")

                # if its in <a>...
                if lis[-2].find('i').find('a') is not None:
                    if len(lis[-2].contents) > 1:
                        band_dict['year1'] = lis[-2].contents[1]
                    else:
                        band_dict['year1'] = 'NONE'

                    band_dict['album1'] = lis[-2].find('i').find('a').get('title')
                # its in <i>
                else:
                    if len(lis[-2].contents) > 1:
                        band_dict['year1'] = lis[-2].contents[1]
                    else:
                        band_dict['year1'] = 'NONE'

                    band_dict['album1'] = lis[-2].contents[0].get_text()
                # REPEAT FOR SECOND ALBUM
                try:
                    if lis[-4].find('a') is not None:
                        if len(lis[-4].contents) > 1:
                            band_dict['year2'] = lis[-4].contents[1]
                        else:
                            band_dict['year2'] = 'NONE'

                        band_dict['album2'] = lis[-4].find('i').find('a').get('title')
                    else:
                        if len(lis[-4].contents) > 1:
                            band_dict['year2'] = lis[-4].contents[1]
                        else:
                            band_dict['year2'] = 'NONE'

                        band_dict['album2'] = lis[-4].contents[0].get_text()
                except IndexError as e:
                    band_dict['year2'] = 'NONE'
                    band_dict['album2'] = 'NONE'
                    print(str(e) + " inserting NONE")

        if band_dict['year1'] is not 'NONE':
            band_dict['year1'] = re.findall('\d{4}', band_dict['year1'])[0]
        if band_dict['year2'] is not 'NONE':
            band_dict['year2'] = re.findall('\d{4}', band_dict['year2'])[0]

        dictionaries.append(band_dict)
        print(str(i) + '. ' + band_dict['band'] + ": ")
        print("    " + band_dict['album1'] + ", " + band_dict['year1'])
        print("    " + band_dict['album2'] + ", " + band_dict['year2'])
    except Exception as e:
        print(band + ' went to shit, LUL')
        print(str(e))
    sleep(random.randrange(3, 5))

# todo: example: devin townsend - extract solo albums as well as devin townsend project albums
''' No Wiki:
ForTiorI
igorrr
pryapisme
roadrunner united(no discography header) 
corpo-mente 
darth vegas 
hentai corporation

Wrong wiki:
shaolin death squad
dead brothers
duct tape mustache

Has headers but none contain "albums"
eminem
'''
