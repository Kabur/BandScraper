import sys
import bs4 as bs
import urllib.parse
import urllib.request

import re

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

# url = 'https://www.google.com/search?q=leprous+new+album'
url = 'https://en.wikipedia.org/wiki/Leprous'
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}

try:
    req = urllib.request.Request(url, headers=headers)
    source = urllib.request.urlopen(req)

    soup = bs.BeautifulSoup(source, 'lxml')
    urls = []
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

except Exception as e:
    print(str(e))

