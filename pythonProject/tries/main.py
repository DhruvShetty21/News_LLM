import requests
from bs4 import BeautifulSoup


URL = "https://timesofindia.indiatimes.com/education"

response = requests.get(URL)
news_data = response.text
soup = BeautifulSoup(news_data,"html.parser")

headline_list = []
headlines = soup.find_all(name="a",rel="noopener")
soup.fina
for headline in headlines:
    data = headline.getText()
    headline_list.append(data)

print(headline_list)


