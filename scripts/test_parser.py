import httpx
from bs4 import BeautifulSoup


def get_comfy_price(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        with httpx.Client(headers=headers, follow_redirects=True) as client:
            response = client.get(url)

            if response.status_code != 200:
                return f"Помилка: статус-код {response.status_code}"

            soup = BeautifulSoup(response.text, "html.parser")

            price_element = soup.find("div", class_="price__current")

            if price_element:

                raw_price = price_element.get_text(strip=True)

                clean_price = "".join(filter(str.isdigit, raw_price))

                return f"Чиста ціна: {clean_price} грн"
            else:
                return "Не вдалося знайти блок з ціною."

    except Exception as e:
        return f"Виникла помилка при запиті: {e}"

test_url = "https://comfy.ua/ua/smartfon-apple-iphone-17-pro-256gb-cosmic-orange.html"
print(get_comfy_price(test_url))
