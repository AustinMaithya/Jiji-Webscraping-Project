import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://jiji.co.ke/video-games-and-consoles"
BASE_URL = "https://jiji.co.ke"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/151.0.0.0 Safari/537.36"
}


def safe_text(element):
    if element is None:
        return ""
    return element.get_text(" ", strip=True)


def fetch_page(url):
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_links():
    console_links = []

    try:
        soup = fetch_page(URL)

        for item in soup.find_all("div", class_="masonry-item"):
            for link in item.find_all("a", href=True):
                full_url = urljoin(BASE_URL, link["href"])
                if full_url not in console_links:
                    console_links.append(full_url)

    except Exception as error:
        print(f"Error fetching links: {error}")

    print(f"\nThe Console links are ({len(console_links)}):")
    for link in console_links:
        print(link)

    return console_links


def get_products(console_links):
    products = []

    for console_link in console_links:
        try:
            soup = fetch_page(console_link)

            product_data = {
                "seller_name": safe_text(soup.find("div", class_="b-seller-block__name")),
                "item": safe_text(
                    soup.find("div", class_="b-advert-title-inner qa-advert-title b-advert-title-inner--h1")
                ),
                "brand": safe_text(soup.find("div", itemprop="brand")),
                "condition": safe_text(soup.find("div", itemprop="itemCondition")),
                "price": safe_text(soup.find("span", class_="qa-advert-price-view-value")),
            }

            products.append(product_data)

        except Exception as error:
            print(f"Error scraping {console_link}: {error}")

    return products


def saving_data(products):
    df = pd.DataFrame(products)
    df.to_csv("consoles.csv", index=False)
    print("Data Saved Successfully")
    return df


def main():
    console_links = get_links()
    products = get_products(console_links)
    df = saving_data(products)

    if not df.empty:
        print(df.head())
    else:
        print("No data was scraped.")


if __name__ == "__main__":
    main()
    

  




















