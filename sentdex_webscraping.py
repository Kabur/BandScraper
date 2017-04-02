import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
import bs4 as bs
import urllib.request

# source = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()
# soup = bs.BeautifulSoup(source, 'lxml')
# js_test = soup.find('p', class_='jstest')
#
# for paragraph in soup.find_all('p'):
#     print(paragraph.text) # or .string
#
# for url in soup.find_all('a'):
#     print(url.get('href'))
#
# body = soup.body
# for paragraph in body.find_all('p'):
#     print(paragraph.text)
#
# for div in soup.find_all('div', class_='body'):
#     print(div.text)

""" reading sitemap """
# source = urllib.request.urlopen('https://pythonprogramming.net/sitemap.xml').read()
# soup = bs.BeautifulSoup(source, 'xml')
#
# for url in soup.find_all('loc'):
#     print(url.text)


# """ reading dynamic js """
# class Client(QWebPage):
#     def __init__(self, url):
#         self.app = QApplication(sys.argv)
#         QWebPage.__init__(self)
#         self.loadFinished.connect(self.on_page_load)
#         self.mainFrame().load(QUrl(url))
#         self.app.exec_()
#
#     def on_page_load(self):
#         self.app.quit()
#
#
# url = 'https://pythonprogramming.net/parsememcparseface/'
# client_response = Client(url)
# source = client_response.mainFrame().toHtml()
# soup = bs.BeautifulSoup(source, 'lxml')
# js_test = soup.find('p', class_='jstest')
# print(js_test.text)
