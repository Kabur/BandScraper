import sys
import bs4 as bs
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

# url = 'https://www.google.com/search?q=leprous+new+album'
url = 'https://en.wikipedia.org/wiki/Leprous'
# url = 'https://en.wikipedia.org/wiki/Ayreon'
# url = 'https://en.wikipedia.org/wiki/The_Algorithm'
# ayreon, leprous, the algorithm
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

''' Learning stuff '''
if False:
    source = html_doc
    try:
        source = html_doc
        soup = bs.BeautifulSoup(source, 'lxml')
        # print(soup.find_all('a', id='link2'))
        # print(soup.find_all(href=re.compile("example"), limit=1))
        # print(soup.find_all(string=re.compile("sisters")))

        # element = soup.find(string="Lacie")
        # print(element)
        # print("*******")
        # parent1 = element.find_parent()
        # print(parent1)
        # print("*******")
        # print(parent1.name)

        body = soup.find("body")
        a = body.find("a")
        print(a)

    except Exception as e:
        print(str(e))
    exit()

''' Actually trying to scrape'''
# try:
req = urllib.request.Request(url, headers=headers)
source = urllib.request.urlopen(req)
soup = bs.BeautifulSoup(source, 'lxml')
# urls = []

''' find discography element '''
discography = soup.find(id='Discography')
disco_parent = discography.find_parent()
sibling = disco_parent.find_next_sibling()
''' Go sideways to find the table with albums '''
while sibling is not None and sibling.name != "table" and sibling.name != "div":
    sibling = sibling.find_next_sibling()

''' Table is present '''
if sibling.name == "table":
    table_rows = sibling.contents
    if table_rows[-2].find("th") is None:
        album = table_rows[-4].find("th")
    else:
        album = table_rows[-2].find("th")

    ''' if there is <a>, extract the album from there '''
    if album.find("a") is not None:
        album = album.find("a")
        print(album.get("title"))  # FINAL
        print(album.get_text())  # FINAL
    elif album.find("i") is not None:
        ''' if there is no <a>, extract the album from <i> '''
        print(album.find("i").get_text())  # FINAL
    else:
        print("DIDNT FIND AN ALBUM, INSPECT WIKI")

    ''' No table, just <ul> and <li> tags'''
else:
    sibling = disco_parent.find_next_sibling()
    print(sibling)
    ''' Go sideways to find uls '''
    while sibling is not None and sibling.name != "ul":
        sibling = sibling.find_next_sibling()
    if sibling is None:
        print("DIDNT FIND AN ALBUM, INSPECT WIKI")
    else:
        lis = sibling.contents
        print(lis[-2].get_text()) # FINAL


        # if there is no tbody, look for <ul>, then go <li> -> <i> -> string or <a>
        # if it was <a>, the date should be its sibling

"""
for url in soup.find_all('a'):
    # href = str(url.get('href'))
    href = repr(url.get('href'))
    # cant use this, Ayreon case doesnt apply
    # How To: find discography, go sideways until <tbody>, now you got your table
    # children tr -> th -> i -> if string, extract name, if <a>, extract title attribute
    # if there is no tbody, look for <ul>, then go <li> -> <i> -> string or <a>
    # if it was <a>, the date should be its sibling
    match = re.search(".*album.*", href)
    if match:
        print(href)
# todo: ended on find_all() in BS documentation

# result = soup.find(class_='story')
"""
# except Exception as e:
#     print(str(e))
