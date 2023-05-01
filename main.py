import requests
from bs4 import BeautifulSoup
import pandas as pd

pages = 5
links = []
for i in range(pages):
    url = f"https://www.dea.gov/what-we-do/news/press-releases?page={i}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the press release titles and dates
    titles = soup.find_all("h3", class_="teaser__heading")

    for title in titles:
        a_tag = title.find("a")
        if a_tag:
            links.append("https://www.dea.gov/" + str(a_tag["href"]))

data = {
    "Title": [],
    "Date": [],
    "Summary": [],
    "Location": [],
    "Link": []
}
for link in links:
    article_url = link
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, "html.parser")

    date = soup.find("div", class_="press__date").text.strip().encode("utf-8")
    title = soup.find("h2", class_="press__title").text.strip().encode("utf-8")
    paragraph_div = soup.find("div", class_="wysiwyg")
    first_paragraph = paragraph_div.find("p").text.strip()
    index = len(first_paragraph)
    for char in ["-", "—", "–", "–"]:
        char_index = first_paragraph.find(char)
        if char_index != -1 and char_index < index:
            index = char_index
            break
    location = first_paragraph[:index].strip().encode("utf-8")

    data["Title"].append(title)
    data["Date"].append(date)
    data["Summary"].append(first_paragraph.encode("utf-8"))
    data["Location"].append(location)
    data["Link"].append(link)

df = pd.DataFrame(data)

df.to_csv("news.csv", index=False)



