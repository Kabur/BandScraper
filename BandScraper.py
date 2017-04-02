import sys
import bs4 as bs
import urllib.parse
import urllib.request

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

    soup = bs.BeautifulSoup(html_doc, 'lxml')

    # for url in soup.find_all('a'):
    #     print(url.get('href'))

    result = soup.find(class_='story')
    print(result)

except Exception as e:
    print(str(e))

