import httpx
from bs4 import BeautifulSoup
from decimal import Decimal
from monitor.models import Product
from dotenv import load_dotenv

load_dotenv()


def update_product_price(product_id):
    product = Product.objects.get(id=product_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    try:
        with httpx.Client(headers=headers, follow_redirects=True, timeout=15.0) as client:
            response = client.get(product.url)

            if response.status_code != 200:
                print(f"Статус помилки: {response.status_code}")
                return False

            soup = BeautifulSoup(response.text, "html.parser")

            # Шукаємо ціну всюди: в Comfy, ITbox або Brain
            price_element = (
                    soup.find("div", class_="price__current") or  # Comfy
                    soup.find("div", class_="price") or  # ITbox
                    soup.find("span", class_="price-number")  # Brain
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

            print(f"Ціну не знайдено за посиланням: {product.url}")
    except Exception as e:
        print(f"Помилка парсингу: {e}")
    return False
