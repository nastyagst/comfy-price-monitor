import httpx
from bs4 import BeautifulSoup
from decimal import Decimal
from monitor.models import Product


def update_product_price(product_id):
    product = Product.objects.get(id=product_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        with httpx.Client(headers=headers, follow_redirects=True) as client:
            response = client.get(product.url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                price_element = soup.find("div", class_="price__current")

                if price_element:
                    raw_price = price_element.get_text(strip=True)
                    clean_price = "".join(filter(str.isdigit, raw_price))

                    product.current_price = Decimal(clean_price)
                    product.save()
                    return True
    except Exception as e:
        print(f"Error updating {product.title}: {e}")
    return False
