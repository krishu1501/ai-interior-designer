from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
from typing import List
from pydantic import BaseModel
import random

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    title: str
    url: str
    image: str
    price: str

# List of user agents to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]

@app.get("/api/search/{query}/{max_results}")
async def search_products(query: str, max_results: int = 10) -> List[Product]:
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    
    url = f"https://www.amazon.in/s?k={query}"
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = []
        print('response1: '+ soup.prettify())

        # Find all product cards
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in results[:max_results]:
            try:
                title_element = item.find('h2').find('a')
                title = title_element.find('span').text.strip()
                url = 'https://www.amazon.in' + title_element['href']
                image = item.find('img', {'class': 's-image'})['src']
                price_element = item.find('span', {'class': 'a-price-whole'})
                price = f"${price_element.text}" if price_element else "N/A"
                
                products.append(Product(
                    title=title,
                    url=url,
                    image=image,
                    price=price
                ))
            except Exception as e:
                logger.warning(f"Error parsing product item: {e}")
                continue
                
        return products
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        return []

if __name__ == "__main__":
    import uvicorn
    import logging

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Run with debug mode
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,  # Enable auto-reload
        log_level="debug"
    )
