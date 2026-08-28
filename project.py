
"""
Jiji Kenya Monitor Scraper

This program:
1. Scrapes monitor listing pages from Jiji Kenya.
2. Extracts unique product URLs.
3. Visits each product page.
4. Extracts product information.
5. Saves the results to a CSV file.
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin




BASE_URL = "https://jiji.co.ke/computer-monitors"
WEBSITE_URL = "https://jiji.co.ke"

START_PAGE = 1
END_PAGE = 69

OUTPUT_FILE = "monitors.csv"
REQUEST_TIMEOUT = 10
from pathlib import Path

OUTPUT_FILE = Path("monitors.csv")

HEADERS = { "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) ""AppleWebKit/537.36 (KHTML, like Gecko) ""Chrome/150.0.0.0 Safari/537.36")}


#EXTRACT PRODUCT URLS

def extract_product_urls():
    """Extract unique monitor product URLs from Jiji listing pages."""

    product_urls = []

    for page in range(START_PAGE, END_PAGE + 1):

        url = f"{BASE_URL}?page={page}&query=monitors"

        print(f"\nRequesting page {page}")
        print(url)

        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            print(f"Page {page} request successful")

        except requests.RequestException as error:
            print(f"Page {page} request failed: {error}")
            continue

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        products = soup.find_all(
            "div",
            class_="masonry-item"
        )

        print(
            f"Products found on page {page}: "
            f"{len(products)}"
        )

        for product in products:

            links = product.find_all(
                "a",
                href=True
            )

            for link in links:

                product_url = urljoin(
                    WEBSITE_URL,
                    link["href"]
                )

                if product_url not in product_urls:
                    product_urls.append(product_url)

    print(
        f"\nTotal unique product URLs extracted: "
        f"{len(product_urls)}"
    )

    return product_urls


#EXTRACT TEXT FROM HTML

def extract_text( soup, tag, class_name=None,itemprop=None):
    """Extract text from an HTML element."""

    if class_name:

        element = soup.find(tag, class_=class_name)

    elif itemprop:
         element = soup.find(tag, itemprop=itemprop)

    else:

        element = soup.find(tag)

    if element:
        return element.get_text(strip=True)

    return "Not available"


#EXTRACT PRODUCT DETAILS

def extract_product_data(product_urls):
    """Extract information from individual product pages."""

    products = []

    total_products = len(product_urls)

    for number, product_url in enumerate(product_urls, start=1):

        print(
            f"\nExtracting product "
            f"{number} of {total_products}"
        )

        try:
            response = requests.get(
                product_url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            # Product title
            title = extract_text( soup,"div", class_name=( "b-advert-title-inner "
                                                          "qa-advert-title "
                                                        "b-advert-title-inner--h1"
                )
            )

            # Product price
            price = extract_text( soup,
                                 "span",
                                    class_name="qa-advert-price-view-value"
                                )

            # Product condition
            condition = extract_text( soup,
                                    "div",
                                     itemprop="itemCondition"
            )

            # Product brand
            brand = extract_text(soup,
                                "div",
                                itemprop="brand"
            )

            # Store address
            store_address = extract_text(soup,
                                        "div",
                                class_name=( "b-store-details__address ""h-mb-10")
            )

            product = {
                "url": product_url,
                "title": title,
                "price": price,
                "condition": condition,
                "brand": brand,
                "store_address": store_address
            }

            products.append(product)

            print(f"Saved: {title}")

        except requests.RequestException as error:

            print(
                f"Request failed for "
                f"{product_url}: {error}"
            )

        except Exception as error:

            print(
                f"Extraction failed for "
                f"{product_url}: {error}"
            )

    return products


#SAVE THE DATA TO CSV FILE

def save_data(products):

    dataframe = pd.DataFrame(products)

    try:

        dataframe.to_csv(
            OUTPUT_FILE,
            index=False
        )

        print(
            f"Successfully saved {len(dataframe)} "
            f"records to {OUTPUT_FILE}"
        )

        return dataframe

    except PermissionError:

        print(
            f"Permission denied: {OUTPUT_FILE}"
        )

        print(
            "Close the CSV file if it is open in Excel "
            "or another program and try again."
        )

        return dataframe


#MAIN PROGRAM

def main():
    """Run the complete scraping process."""

    print("=" * 60)
    print("JIJI KENYA MONITOR SCRAPER")
    print("=" * 60)

    # Step 1: Extract product URLs
    product_urls = extract_product_urls()

    if not product_urls:

        print("\nNo product URLs were found.")
        return

    # Step 2: Extract product information
    products = extract_product_data(
        product_urls
    )

    if not products:

        print("\nNo product information was extracted.")
        return

    # Step 3: Save data
    dataframe = save_data(products)

    # Step 4: Display results
    print("\n" + "=" * 60)
    print("SCRAPING COMPLETED")
    print("=" * 60)

    print("\nFirst five products:")
    print(dataframe.head())

    print(
        f"\nTotal products extracted: "
        f"{len(dataframe)}"
    )


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()