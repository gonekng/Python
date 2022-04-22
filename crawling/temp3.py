from bs4 import BeautifulSoup
soup = BeautifulSoup(open("index2.html"), 'html.parser')

for link in soup.find_all('a'):
    print(link.get('href'))

print(soup.get_text())
