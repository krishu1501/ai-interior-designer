from fastapi import APIRouter, File, UploadFile, Form
from ..services.amazon_service import AmazonService
from ..services.gemini_service import GeminiService
from ..models.schemas import RoomDesignResponse, Product
from ..config import settings
from PIL import Image
from io import BytesIO
from typing import List

router = APIRouter()
gemini_service = GeminiService(settings.GEMINI_API_KEY)

@router.get("/search/{query}/{max_results}", response_model=List[Product])
async def search_products(query: str, max_results: int = 10):
    return await AmazonService.search_products(query, max_results)

@router.post("/design-room", response_model=RoomDesignResponse)
async def design_room(
    image: UploadFile = File(...),
    theme: str = Form(default="modern")
):
    # Process image
    image_content = await image.read()
    pil_image = Image.open(BytesIO(image_content))
    
    # Get product suggestions
    suggestions = await gemini_service.get_product_suggestions(pil_image, theme)
    
    # Get Amazon products for suggestions
    for suggestion in suggestions[:10]:
        products = await AmazonService.search_products(suggestion.newProduct, 1)
        if products:
            suggestion.amazonDetails = products[0]
    
    # Generate new room image
    new_image = await gemini_service.generate_room_image(pil_image, suggestions)
    
    return RoomDesignResponse(
        suggestions=suggestions,
        newImage=new_image
    )
