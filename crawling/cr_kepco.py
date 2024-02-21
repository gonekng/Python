import os
import requests
from lxml import html

file_names = []
file_links = []

for i in range(5):
    url = f"https://home.kepco.co.kr/kepco/KO/ntcob/list.do?pageIndex={i+1}&boardSeq=0&boardCd=BRD_000097&menuCd=FN05030101&parnScrpSeq=0&categoryCdGroup=&regDateGroup1="
    response = requests.get(url)
    tree = html.fromstring(response.content)

    print("page:", i+1)
    rows = tree.xpath('//*[@id="content"]/div[4]/div[1]/table/tbody/tr')
    if len(rows) > 0:
        for row in rows:
            file = row.xpath('.//a[@class="ico_excel"]')[0]
            file_name = file.attrib['title']
            file_names.append(file_name)
            file_link = "https://home.kepco.co.kr" + file.attrib['href']
            file_links.append(file_link)
    else:
        print("no row")

for i, link in enumerate(file_links):
    response = requests.get(link)
    with open(os.path.join("전력통계월보_한전", file_names[i]), "wb") as file:
        file.write(response.content)
    print(f"- {file_names[i]} downloaded.")
