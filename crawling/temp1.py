from bs4 import BeautifulSoup
soup = BeautifulSoup(open("index2.html"), 'html.parser')

print(soup.prettify())
