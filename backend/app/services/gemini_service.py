from google import genai
from PIL import Image
import base64
from typing import List, Tuple
from ..models.schemas import ProductSuggestion, ProductSuggestionResponse

class GeminiService:
    def __init__(self, api_key: str):
        # genai.configure(api_key=api_key)
        self.client = genai.Client(api_key=api_key)

    async def get_product_suggestions(self, image: Image, theme: str) -> List[ProductSuggestion]:
        prompt = f'''You are an interior designer. I want to buy new items for my room to add or replace products 
        or furniture. Suggest item names to be bought. Limit item name to 3 words. If the new item is replacing one of the current items form 
        the room, it should also have name of current object that needs to be replaced from the image of room. 
        The goal is to have the room look based on the theme {theme}'''

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image],
            config={
                "response_mime_type": "application/json",
                "response_schema": list[ProductSuggestionResponse],
            }
        )
        productSuggestions: list[ProductSuggestionResponse] = response.parsed
        # return [ProductSuggestion(**item) for item in response.parsed]
        return await self.map_suggestions(productSuggestions)

    async def generate_room_image(self, image: Image, suggestions: List[ProductSuggestion]) -> str:
        prompt = f"Using the room image, create a photorealistic view replacing or adding these items: {str(suggestions)}"
        
        response = self.client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=[prompt, image]
        )
        
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                return base64.b64encode(part.inline_data.data).decode()
        
        raise ValueError("No image generated in response")
    
    async def map_suggestions(self, response_parsed: List[ProductSuggestionResponse]) -> List[ProductSuggestion]:
        """
        Maps a list of ProductSuggestionResponse objects to a list of ProductSuggestion objects.
        """
        mapped_suggestions = []
        for suggestion_response in response_parsed:
            new_suggestion = ProductSuggestion(
                oldProduct=suggestion_response.oldProduct,
                newProduct=suggestion_response.newProduct,
                amazonDetails=None  # Set to None as this info isn't available
            )
            mapped_suggestions.append(new_suggestion)
        return mapped_suggestions
