import os
from typing import List, Optional
import json
import asyncio
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL", "llama-3.2-11b-vision-preview")
API_KEY = os.getenv("API_KEY", "")

groq = Groq(api_key=API_KEY)


# Data model for LLM to generate
class ServingSize(BaseModel):
    amount: float
    unit: str


class Macronutrient(BaseModel):
    amount: float
    unit: str
    daily_value: Optional[float]
    breakdown: Optional[dict]


class NutritionFacts(BaseModel):
    calories: int
    macronutrients: dict
    vitamins_and_minerals: List[dict]


class ProductDetails(BaseModel):
    food_name: str
    serving_size: ServingSize


class AdditionalInfo(BaseModel):
    ingredients: Optional[List[str]]
    allergens: Optional[List[str]]
    storage_instructions: Optional[str]
    preparation_instructions: Optional[str]


class NutritionInfo(BaseModel):
    product_details: ProductDetails
    nutrition_facts: NutritionFacts
    additional_info: Optional[AdditionalInfo]


async def get_nutrition_info(image_url: str) -> NutritionInfo:
    system_prompt = (
        "Extract comprehensive nutritional information from the food label image. "
        "Structure the output in JSON format, including fields even if values are missing (use 0 or null). "
        "Ensure all units are standardized (g, mg, mcg, %DV) and include daily value percentages where available. "
        "Handle abbreviations appropriately (e.g., 'sat.' → 'saturated', 'cholest.' → 'cholesterol'). "
        "If any field is missing from the label, use 0 for numerical values and empty strings/null for text fields."
    )

    chat_completion = await asyncio.to_thread(
        groq.chat.completions.create,
        messages=[
            {
                "role": "system",
                "content": f"{system_prompt}\nThe JSON object must use the schema: {json.dumps(NutritionInfo.model_json_schema(), indent=2)}",
            },
            {
                "role": "user",
                "content": image_url,
            },
        ],
        model=MODEL,
        temperature=0.2,
        stream=False,
        response_format={"type": "json_object"},
    )

    response = chat_completion.choices[0].message.content
    tokens = chat_completion.usage
    print(tokens)

    print(response)
    return NutritionInfo.model_validate_json(response)


def print_nutrition_info(nutrition_info: NutritionInfo):
    print("Product Details:")
    print(f"Food Name: {nutrition_info.product_details.food_name}")
    print(
        f"Serving Size: {nutrition_info.product_details.serving_size.amount} {nutrition_info.product_details.serving_size.unit}"
    )

    print("\nNutrition Facts:")
    print(f"Calories: {nutrition_info.nutrition_facts.calories}")
    for nutrient, details in nutrition_info.nutrition_facts.macronutrients.items():
        if isinstance(details, dict):
            print(
                f"{nutrient.capitalize()}: {details['amount']} {details['unit']} (Daily Value: {details.get('daily_value', 'N/A')})"
            )
            if "breakdown" in details:
                for sub_nutrient, sub_amount in details["breakdown"].items():
                    print(f"  {sub_nutrient.capitalize()}: {sub_amount}")
        else:
            print(f"{nutrient.capitalize()}: {details}")

    print("\nVitamins and Minerals:")
    for vitamin in nutrition_info.nutrition_facts.vitamins_and_minerals:
        print(
            f"{vitamin['name']}: {vitamin['amount']} {vitamin['unit']} (Daily Value: {vitamin.get('daily_value', 'N/A')})"
        )

    if nutrition_info.additional_info:
        print("\nAdditional Info:")
        if nutrition_info.additional_info.ingredients:
            print(
                f"Ingredients: {', '.join(nutrition_info.additional_info.ingredients)}"
            )
        if nutrition_info.additional_info.allergens:
            print(f"Allergens: {', '.join(nutrition_info.additional_info.allergens)}")
        if nutrition_info.additional_info.storage_instructions:
            print(
                f"Storage Instructions: {nutrition_info.additional_info.storage_instructions}"
            )
        if nutrition_info.additional_info.preparation_instructions:
            print(
                f"Preparation Instructions: {nutrition_info.additional_info.preparation_instructions}"
            )


async def main():
    image_url = "https://www.hdstech.com.au/wp-content/uploads/2019/03/joooooooooo.jpg"
    nutrition_info = await get_nutrition_info(image_url)
    print_nutrition_info(nutrition_info)


if __name__ == "__main__":
    asyncio.run(main())
