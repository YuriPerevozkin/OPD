import requests
from bs4 import BeautifulSoup as bs


def parse():
    url = "https://spb.sutochno.ru/flats"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }

    page = requests.get(url, headers=headers)
    soup = bs(page.text, "html.parser")

    objects_list = soup.find_all("div", class_="objects-list")[0]

    with open("flats.xlsx", "w") as f:
        for card in objects_list.find_all("div", class_="card"):
            card_content = card.find("div", class_="card-content")

            flat = card_content.find("a", class_="card-content__object-type").text

            f.write(f"{flat};")


if __name__ == "__main__":
    parse()
