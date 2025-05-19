import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_etsy(search_term):
    url = f"https://www.etsy.com/search?q={search_term.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    products = soup.find_all("li", class_="wt-list-unstyled")
    data = []

    for product in products[:10]:
        title = product.find("h3")
        price = product.find("span", class_="currency-value")
        rating = product.find("span", class_="screen-reader-only")

        if title and price:
            data.append({
                "Title": title.get_text(strip=True),
                "Price": price.get_text(strip=True),
                "Rating": rating.get_text(strip=True) if rating else "N/A"
            })

    df = pd.DataFrame(data)
    filename = f"{search_term.replace(' ', '_')}_etsy_results.xlsx"
    df.to_excel(filename, index=False)
    print(f"Saved: {filename}")

# Example usage
scrape_etsy("handmade necklace")
