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


with open("bands.txt", 'r') as file:
    bands = file.readlines()

# albums = []
dictionaries = []
for band in bands:
    band_dict = {'band': band[:-1]}
    query = "site:en.wikipedia.org+" + band + "band"
    query = query.replace(" ", "+")
    response = requests.get("https://www.google.com/search?q=" + query)
    soup = bs.BeautifulSoup(response.text, "lxml")

    link = soup.find('h3', attrs={'class': 'r'}) # Guides BS to h3 class "r" where green Wikipedia URLs are located, then prints URLs
    # print(soup.prettify())

    link = link.find("a").get("href")
    link = link[7:].split("&")[0] # [7:] strips the /url?q= prefix, split removes garbage in link after &
    source = requests.get(link)
    soup = bs.BeautifulSoup(source.content, 'lxml')

    # ''' find discography element '''
    discography = soup.find(id='Discography')
    disco_parent = discography.find_parent()
    # sibling = disco_parent.find_next_sibling()
    # ''' Go sideways to find the table with albums '''
    # while sibling is not None and sibling.name != "table":
    #     sibling = sibling.find_next_sibling()

    sibling = disco_parent.find_next_sibling()
    while re.match('.*[aA]lbums.*', sibling.find('span').get_text()) is None:
        sibling = sibling.find_next_sibling()

    ''' 
    Type 1:
    Table is present 
    '''
    if sibling.name == "table":
        table_rows = sibling.contents
        # in case there is a junk table row -> cut it
        if table_rows[-2].find("th") is None:
            table_rows = table_rows[:-2]

        th = table_rows[-2].find('th')
        # if its in <a>
        if th.find('i').find("a") is not None:
            band_dict['album1'] = th.find('i').find("a").get('title')
            # if its just in <i>
        else:
            band_dict['album1'] = th.find('i').get_text()
        td = th.find_next_sibling()
        band_dict['year1'] = re.findall('\d{4}', td.get_text())[0]

        # ''' same shit for the second album, should put it to a function prolly xD '''
        try:
            th = table_rows[-4].find('th')
            # if its in <a>
            if th.find('i').find("a") is not None:
                band_dict['album2'] = th.find('i').find("a").get('title')
                # if its just in <i>
            else:
                band_dict['album2'] = th.find('i').get_text()
            td = th.find_next_sibling()
            band_dict['year2'] = re.findall('\d{4}', td.get_text())[0]
        except IndexError as e:
            band_dict['year2'] = 'NONE'
            band_dict['album2'] = 'NONE'
            print(str(e))

        ''' 
        TYPE 2:
        No table, just <ul> and <li> tags
        '''
    else:
        sibling = disco_parent.find_next_sibling()
        # ''' Go sideways to find uls '''
        while sibling is not None and sibling.name != "ul":
            sibling = sibling.find_next_sibling()
        if sibling is None:
            print("DIDNT FIND AN ALBUM, INSPECT WIKI")
        else:
            lis = sibling.contents

            # sometimes there is a junk tag instead of the year -> cut
            if re.match('.*\d{4}.*', str(lis[-2].contents[1])) is None:
                del lis[-2].contents[1]
                print("Kappa")

            if lis[-2].find('i').find('a') is not None:  # if its in <a>...
                band_dict['year1'] = lis[-2].contents[1]
                band_dict['album1'] = lis[-2].find('i').find('a').get('title')
            else:  # its in <i>
                band_dict['year1'] = lis[-2].contents[1]
                band_dict['album1'] = lis[-2].contents[0].get_text()
            try:
                if lis[-4].find('a') is not None:
                    band_dict['year2'] = lis[-4].contents[1]
                    band_dict['album2'] = lis[-4].find('i').find('a').get('title')
                else:
                    band_dict['year2'] = lis[-4].contents[1]
                    band_dict['album2'] = lis[-4].contents[0].get_text()
            except IndexError as e:
                band_dict['year2'] = 'NONE'
                band_dict['album2'] = 'NONE'
                print(str(e) + " inserting NONE")

    band_dict['year1'] = re.findall('\d{4}', band_dict['year1'])[0]
    if band_dict['year2'] is not 'NONE':
        band_dict['year2'] = re.findall('\d{4}', band_dict['year2'])[0]

    dictionaries.append(band_dict)
    print(band_dict['band'] + ": ")
    print("    " + band_dict['album1'] + ", " + band_dict['year1'])
    print("    " + band_dict['album2'] + ", " + band_dict['year2'])

# for item in dictionaries:
#     print(item['band'] + ": ")
#     print("    " + item['album1'] + ", " + item['year1'])
#     print("    " + item['album2'] + ", " + item['year2'])

# todo: (DONE - needs testing) only extract after Studio albums or Albums header, not right after discography
# todo: test on all bands
