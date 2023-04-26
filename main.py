import requests
from bs4 import BeautifulSoup


url = "https://www.dea.gov/what-we-do/news/press-releases?f%5B0%5D=press_year%3A2020&page=0"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
print(soup)

# Find all the press release titles and dates
titles = soup.find_all("h3", class_="teaser__heading")
dates = soup.find_all("div", class_="teaser__date")
links = []
for title in titles:
    a_tag = title.find("a")
    if a_tag:
        links.append(a_tag)

# Print the title and date of each press release
for i in range(len(titles)):
    title = titles[i].text.strip()
    date = dates[i].text.strip()
    link = links[i]["href"]
    print(f"{date} - {title} - https://www.dea.gov/{link}")
