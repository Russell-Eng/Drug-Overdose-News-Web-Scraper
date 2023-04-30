import requests
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.dea.gov/what-we-do/news/press-releases?page=0"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
# print(soup)

# Find all the press release titles and dates
titles = soup.find_all("h3", class_="teaser__heading")
dates = soup.find_all("div", class_="teaser__date")
links = []
for title in titles:
    a_tag = title.find("a")
    if a_tag:
        links.append("https://www.dea.gov/" + str(a_tag["href"]))

press_summary = []
data = {
    "Title": [],
    "Date": [],
    "Summary": [],
    "Location": []
}
for link in links:
    article_url = link
    response = requests.get(article_url)
    soup = BeautifulSoup(response.content, "html.parser")

    date = soup.find("div", class_="press__date").text.strip()
    title = soup.find("h2", class_="press__title").text.strip()
    paragraph_div = soup.find("div", class_="wysiwyg")
    first_paragraph = paragraph_div.find("p").text.strip()
    index = len(first_paragraph)
    for char in ["-", "—", "–", "–"]:
        char_index = first_paragraph.find(char)
        if char_index != -1 and char_index < index:
            index = char_index
            break
    location = first_paragraph[:index].strip()

    data["Title"].append(title)
    data["Date"].append(date)
    data["Summary"].append(first_paragraph)
    data["Location"].append(location)
    # press_summary.append(f"{date} - {title} - {first_paragraph}")

# print(press_summary)
df = pd.DataFrame(data)
print(df["Location"])


# Print the title and date of each press release
# for i in range(len(titles)):
#     title = titles[i].text.strip()
#     date = dates[i].text.strip()
#     # link = links[i]["href"]
#     print(f"{date} - {title} - {links[i]}")
