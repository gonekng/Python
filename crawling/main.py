from bs4 import BeautifulSoup
def main():
    # Convert index.html to BeautifulSoup Object
	soup = BeautifulSoup(open("index.html", encoding='UTF-8'), "html.parser")
	print(type(soup))

	print(soup.find("p"))
	print("----------------")
	print(soup.find_all("p"))
	print("----------------")
	print(soup.find("div", class_ = "chapter02"))
	print("----------------")
	print(soup.find("div", id = "main").find("p").get_text())

if __name__ == "__main__":
	main()
