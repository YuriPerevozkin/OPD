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
        f.write("Название;Стоимость;Вместимость;Площадь;")

        for card in objects_list.find_all("div", class_="card"):
            card_content = card.find("div", class_="card-content")
            card_prices = card.find("div", class_="card-prices")

            flat_name = card_content.find("a", class_="card-content__object-type").text
            flat_price = card_prices.find("div", class_="card-prices__bottom").find("div", class_="price-order").find_all("span")[1].text
            flat_capacity = card_content.find("div", class_="card-content__facilities").find("a").find("p").text.strip()
            flat_area = card_content.find("div", class_="facilities__size").find("span").find("span").text

            f.write(f"{flat_name};{flat_price};{flat_capacity};{flat_area};")


if __name__ == "__main__":
    parse()
