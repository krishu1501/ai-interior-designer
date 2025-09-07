import random
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
import logging
from ..models.schemas import Product

logger = logging.getLogger(__name__)

class AmazonService:
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]

    @classmethod
    async def search_products(cls, query: str, max_results: int = 10) -> List[Product]:
        headers = {
            'User-Agent': random.choice(cls.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        url = f"https://www.amazon.in/s?k={query}"
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            return cls._parse_products(soup, max_results)
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            return []

    @classmethod
    def _parse_products(cls, soup: BeautifulSoup, max_results: int) -> List[Product]:
        products = []
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in results[:max_results]:
            try:
                product = cls._parse_product_item(item)
                if product:
                    products.append(product)
            except Exception as e:
                logger.warning(f"Error parsing product item: {e}")
                continue
        
        return products

    @staticmethod
    def _parse_product_item(item) -> Optional[Product]:
        title_element = item.select_one('h2 .a-link-normal')
        if not title_element:
            return None

        return Product(
            title=title_element.find('span').text.strip(),
            url='https://www.amazon.in' + title_element['href'],
            image=item.select_one('img.s-image')['src'] if item.select_one('img.s-image') else "",
            price=f"₹{item.select_one('.a-price .a-price-whole').text}" if item.select_one('.a-price .a-price-whole') else "N/A",
            rating=item.select_one('.a-icon-star-mini').find('span').text if item.select_one('.a-icon-star-mini') else "",
            reviews_count=item.select_one('a[href*="#customerReviews"] span').text if item.select_one('a[href*="#customerReviews"] span') else "",
            mrp=item.select_one('.a-price.a-text-price[data-a-strike="true"] .a-offscreen').text if item.select_one('.a-price.a-text-price[data-a-strike="true"] .a-offscreen') else "",
            discount=item.select_one('.a-row span:contains("%")').text.strip() if item.select_one('.a-row span:contains("%")') else "",
            delivery_date=item.select_one('.udm-primary-delivery-message .a-text-bold').text if item.select_one('.udm-primary-delivery-message .a-text-bold') else ""
        )
