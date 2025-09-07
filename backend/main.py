from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from typing import List
from pydantic import BaseModel

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

@app.get("/api/search/{query}/{max_results}")
async def search_products(query: str, max_results: int = 10) -> List[Product]:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get(f"https://www.amazon.in/s?k={query}")
        products = []
        
        product_cards = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
        
        for card in product_cards[:max_results]:
            try:
                title = card.find_element(By.CSS_SELECTOR, "h2 a span").text
                url = card.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")
                image = card.find_element(By.CSS_SELECTOR, "img.s-image").get_attribute("src")
                price = card.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
                
                products.append(Product(
                    title=title,
                    url=url,
                    image=image,
                    price=f"${price}"
                ))
            except:
                continue
                
        return products
    finally:
        driver.quit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
