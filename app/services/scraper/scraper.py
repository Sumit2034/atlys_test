import requests
from bs4 import BeautifulSoup
from typing import List
from fastapi import HTTPException, status
import time

from app.models.product import ProductDocument
from app.request_validations.scraper_params import ScraperParams


class Scraper:
    def __init__(self, scraper_params: ScraperParams = None):
        self.base_url = scraper_params.url
        self.max_pages = scraper_params.pages
        self.proxy = scraper_params.proxy
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.session = requests.Session()
        if scraper_params.proxy:
            self.session.proxies = {'http': scraper_params.proxy, 'https': scraper_params.proxy}
        self.retry_attempts = 3
        self.retry_delay = 5
    
    """method to retry the page if page is not working"""
    async def fetch_page(self, url: str) -> BeautifulSoup:
        for _ in range(self.retry_attempts):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
            except requests.RequestException:
                time.sleep(self.retry_delay)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to fetch the page after retries")
    
    """method to scrape the list of products upto given pages"""
    async def scrape(self) -> List[ProductDocument]:
        products = []

        """This loop is for pagination"""
        for page in range(1, self.max_pages + 1):
            time.sleep(1)
            url = self.base_url
            if page >1:
                url = f"{self.base_url}/page/{page}/"

            soup = await self.fetch_page(url)
            page_products = soup.select_one('#mf-shop-content > ul')
            product_cards = page_products.find_all('li')

            """This loop is to iterate on each card and collect the data"""
            for card in product_cards:
                try:
                    name_tag  = card.select_one('.mf-product-thumbnail img')
                    if name_tag:
                        name = name_tag.get('title').strip()
                    else:
                        name = "Name not found"
                    price_tag = card.select_one('.mf-product-price-box .price .woocommerce-Price-amount bdi')
                    if price_tag:
                        price_text = price_tag.get_text(strip=True).replace("₹", "").replace(",", "")
                        try:
                            price = float(price_text)
                        except ValueError:
                            price = 'Invalid price'
                    else:
                        price = '0.0'

                    img_tag = card.select_one('.mf-product-thumbnail a')
                    img_tag_ = img_tag.select_one('img')
                    if img_tag_:
                        img_url = img_tag_.get('data-lazy-src') or img_tag_.get('src') or 'No image found'
                    else:
                        img_url = 'No image found'
                    
                    products.append(ProductDocument(name=name, price=price, image=img_url))
                except Exception as e:
                    print(f"Error processing card: {e} {url} {card}")
        return products
