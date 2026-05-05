import httpx
from bs4 import BeautifulSoup
from decimal import Decimal
from monitor.models import Product
from dotenv import load_dotenv

load_dotenv()


def update_product_price(product_id):
    product = Product.objects.get(id=product_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    try:
        with httpx.Client(
            headers=headers, follow_redirects=True, timeout=15.0
        ) as client:
            response = client.get(product.url)

            if response.status_code != 200 and len(response.text) < 5000:
                print(f"Помилка: статус {response.status_code}, контент замалий")
                return False

            soup = BeautifulSoup(response.text, "html.parser")

            price_element = (
                soup.find("span", class_="price-number")  # Brain
                or soup.find("div", class_="price__current")  # Comfy
                or soup.find("div", class_="price")  # ITbox
            )

            if price_element:
                raw_price = price_element.get_text(strip=True)
                clean_price = "".join(filter(str.isdigit, raw_price))

                if clean_price:
                    product.current_price = Decimal(clean_price)

                    title_element = soup.find("h1")
                    if title_element:
                        product.title = title_element.get_text(strip=True)

                    product.save()
                    return True

            print(f"Ціну не знайдено на сторінці")
    except Exception as e:
        print(f"Error: {e}")
    return False
