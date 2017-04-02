# get all google result links
print("**************")
links = []
for item in soup.find_all('h3', attrs={'class': 'r'}):
    links.append(item.a['href'][7:])
    # [7:] strips the /url?q= prefix
    # Guides BS to h3 class "r" where green Wikipedia URLs are located, then prints URLs
    # Limiter code to only pull top 5 results
print(links)

""" reading sitemap """
# source = urllib.request.urlopen('https://pythonprogramming.net/sitemap.xml').read()
# soup = bs.BeautifulSoup(source, 'xml')
#
# for url in soup.find_all('loc'):
#     print(url.text)


""" using variables for search queries"""
# values = {'q': 'leprous new album'}
# values_encoded = urllib.parse.urlencode(values)
# values_encoded = values_encoded.encode('utf-8')
# req = urllib.request.Request(url, values_encoded)
