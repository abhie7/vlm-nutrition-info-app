import os
import asyncio
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL", "llama-3.2-11b-vision-preview")
API_KEY = os.getenv(
    "API_KEY", "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"
)

groq = Groq(api_key=API_KEY)


async def get_nutrition_info(image_url: str):
    chat_completion = await asyncio.to_thread(
        groq.chat.completions.create,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
Extract comprehensive nutritional information from the food label image. Structure the output in JSON format, including fields even if values are missing (use 0 or null). Ensure all units are standardized (g, mg, mcg, %DV) and include daily value percentages where available. Handle abbreviations appropriately (e.g., 'sat.' → 'saturated', 'cholest.' → 'cholesterol'). If any field is missing from the label, use 0 for numerical values and empty strings/null for text fields. Add your confidence score precisely upto 2 floating points to the metadata field. Please include the health insights from your side if possible.

Response Structure:
{
    "metadata": {
        "confidence_score": "float or null",
        "error_status": "boolean or null"
    },
    "product_details": {
        "serving_size": {
            "amount": "float or null",
            "unit": "string"
            "type": "string or null", # e.g., 'calories', 'serving', 'container'
        }
    },
    "total_calories": "integer",
    "nutrients": {
        "total_fat": {
            "amount": "float or null",
            "unit": "g",
            "daily_value_percentage": "float or null",
            "group": "fats",
            "category": "macronutrient",
            "sub_nutrients": {
                "saturated_fat": {
                    "amount": "float or null",
                    "unit": "g",
                    "daily_value_percentage": "float or null",
                    "group": "fats",
                    "category": "macronutrient"
                },
                "trans_fat": {
                    "amount": "float or null",
                    "unit": "g",
                    "daily_value_percentage": "float or null",
                    "group": "fats",
                    "category": "macronutrient"
                }
            }
        },
        "cholesterol": {
            "amount": "float or null",
            "unit": "mg",
            "daily_value_percentage": "float or null",
            "group": "fats",
            "category": "macronutrient"
        },
        "carbohydrates": {
            "amount": "float or null",
            "unit": "g",
            "daily_value_percentage": "float or null",
            "group": "carbohydrates",
            "category": "macronutrient",
            "sub_nutrients": {
                "dietary_fiber": {
                    "amount": "float or null",
                    "unit": "g",
                    "daily_value_percentage": "float or null",
                    "group": "carbohydrates",
                    "category": "macronutrient"
                },
                "total_sugar": {
                    "amount": "float or null",
                    "unit": "g",
                    "daily_value_percentage": "float or null",
                    "group": "carbohydrates",
                    "category": "macronutrient"
                },
                "added_sugar": {
                    "amount": "float or null",
                    "unit": "g",
                    "daily_value_percentage": "float or null",
                    "group": "carbohydrates",
                    "category": "macronutrient"
                }
            }
        },
        "protein": {
            "amount": "float or null",
            "unit": "g",
            "daily_value_percentage": "float or null",
            "group": "protein",
            "category": "macronutrient"
        },
        "sodium": {
            "amount": "float or null",
            "unit": "mg",
            "daily_value_percentage": "float or null",
            "group": "mineral",
            "category": "micronutrient"
        },
        "calcium": {
            "amount": "float or null",
            "unit": "mg",
            "daily_value_percentage": "float or null",
            "group": "mineral",
            "category": "micronutrient"
        },
        "iron": {
            "amount": "float or null",
            "unit": "mg",
            "daily_value_percentage": "float or null",
            "group": "mineral",
            "category": "micronutrient"
        },
        "vitamins": [
            {
                "vitamin_type": "string", # e.g., 'A', 'B', 'C', 'D', 'E', 'K'
                "amount": "float",
                "unit": "mg",
                "daily_value_percentage": "float or null",
                "group": "vitamins",
                "category": "micronutrient"
            }
        ],
    },
    "ingredients": ["string"] or null,
    "allergens": ["string"] or null
}
""",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            },
        ],
        model=MODEL,
        temperature=0.2,
        stream=False,
        response_format={
            "type": "json_object",
            "schema": {
                "type": "object",
                "properties": {
                    "metadata": {
                        "type": "object",
                        "properties": {
                            "confidence_score": {"type": ["number", "null"]},
                            "error_status": {"type": ["boolean", "null"]},
                        },
                        "required": ["confidence_score"],
                    },
                    "product_details": {
                        "type": "object",
                        "properties": {
                            "serving_size": {
                                "type": "object",
                                "properties": {
                                    "amount": {"type": ["number", "null"]},
                                    "unit": {"type": "string"},
                                    "type": {"type": ["string", "null"]},
                                },
                                "required": ["amount", "unit"],
                            },
                        },
                        "required": ["serving_size"],
                    },
                    "total_calories": {"type": "integer"},
                    "nutrients": {
                        "type": "object",
                        "properties": {
                            "total_fat": {
                                "type": "object",
                                "properties": {
                                    "amount": {"type": ["number", "null"]},
                                    "unit": {"type": "string"},
                                    "daily_value_percentage": {
                                        "type": ["number", "null"]
                                    },
                                    "group": {"type": "string"},
                                    "category": {"type": "string"},
                                    "sub_nutrients": {
                                        "type": "object",
                                        "properties": {
                                            "saturated_fat": {
                                                "type": "object",
                                                "properties": {
                                                    "amount": {
                                                        "type": ["number", "null"]
                                                    },
                                                    "unit": {"type": "string"},
                                                    "daily_value_percentage": {
                                                        "type": ["number", "null"]
                                                    },
                                                    "group": {"type": "string"},
                                                    "category": {"type": "string"},
                                                },
                                            },
                                            "trans_fat": {
                                                "type": "object",
                                                "properties": {
                                                    "amount": {
                                                        "type": ["number", "null"]
                                                    },
                                                    "unit": {"type": "string"},
                                                    "daily_value_percentage": {
                                                        "type": ["number", "null"]
                                                    },
                                                    "group": {"type": "string"},
                                                    "category": {"type": "string"},
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                            "cholesterol": {
                                "type": "object",
                                "properties": {
                                    "amount": {"type": ["number", "null"]},
                                    "unit": {"type": "string"},
                                    "daily_value_percentage": {
                                        "type": ["number", "null"]
                                    },
                                    "group": {"type": "string"},
                                    "category": {"type": "string"},
                                },
                            },
                            "carbohydrates": {
                                "type": "object",
                                "properties": {
                                    "amount": {"type": ["number", "null"]},
                                    "unit": {"type": "string"},
                                    "daily_value_percentage": {
                                        "type": ["number", "null"]
                                    },
                                    "group": {"type": "string"},
                                    "category": {"type": "string"},
                                    "sub_nutrients": {
                                        "type": "object",
                                        "properties": {
                                            "dietary_fiber": {
                                                "type": "object",
                                                "properties": {
                                                    "amount": {
                                                        "type": ["number", "null"]
                                                    },
                                                    "unit": {"type": "string"},
                                                    "daily_value_percentage": {
                                                        "type": ["number", "null"]
                                                    },
                                                    "group": {"type": "string"},
                                                    "category": {"type": "string"},
                                                },
                                            },
                                            "total_sugar": {
                                                "type": "object",
                                                "properties": {
                                                    "amount": {
                                                        "type": ["number", "null"]
                                                    },
                                                    "unit": {"type": "string"},
                                                    "daily_value_percentage": {
                                                        "type": ["number", "null"]
                                                    },
                                                    "group": {"type": "string"},
                                                    "category": {"type": "string"},
                                                },
                                            },
                                            "added_sugar": {
                                                "type": "object",
                                                "properties": {
                                                    "amount": {
                                                        "type": ["number", "null"]
                                                    },
                                                    "unit": {"type": "string"},
                                                    "daily_value_percentage": {
                                                        "type": ["number", "null"]
                                                    },
                                                    "group": {"type": "string"},
                                                    "category": {"type": "string"},
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                            "protein": {
                                "type": "object",
                                "properties": {
                                    "amount": {"type": ["number", "null"]},
                                    "unit": {"type": "string"},
                                    "daily_value_percentage": {
                                        "type": ["number", "null"]
                                    },
                                    "group": {"type": "string"},
                                    "category": {"type": "string"},
                                },
                            },
                            "sodium": {
                                "type": "object",
                                "properties": {
                                    "amount": {"type": ["number", "null"]},
                                    "unit": {"type": "string"},
                                    "daily_value_percentage": {
                                        "type": ["number", "null"]
                                    },
                                    "group": {"type": "string"},
                                    "category": {"type": "string"},
                                },
                            },
                            "calcium": {
                                "type": "object",
                                "properties": {
                                    "amount": {"type": ["number", "null"]},
                                    "unit": {"type": "string"},
                                    "daily_value_percentage": {
                                        "type": ["number", "null"]
                                    },
                                    "group": {"type": "string"},
                                    "category": {"type": "string"},
                                },
                            },
                            "iron": {
                                "type": "object",
                                "properties": {
                                    "amount": {"type": ["number", "null"]},
                                    "unit": {"type": "string"},
                                    "daily_value_percentage": {
                                        "type": ["number", "null"]
                                    },
                                    "group": {"type": "string"},
                                    "category": {"type": "string"},
                                },
                            },
                            "vitamins": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "vitamin_type": {"type": "string"},
                                        "amount": {"type": "number"},
                                        "unit": {"type": "string"},
                                        "daily_value_percentage": {
                                            "type": ["number", "null"]
                                        },
                                        "group": {"type": "string"},
                                        "category": {"type": "string"},
                                    },
                                },
                            },
                        },
                    },
                    "ingredients": {
                        "type": ["array", "null"],
                        "items": {"type": "string"},
                    },
                    "allergens": {
                        "type": ["array", "null"],
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "metadata",
                    "product_details",
                    "total_calories",
                    "nutrients",
                ],
            },
        },
    )

    response = chat_completion.choices[0].message.content
    completion_time = round(chat_completion.usage.completion_time, 2)
    completion_tokens = chat_completion.usage.completion_tokens
    prompt_tokens = chat_completion.usage.prompt_tokens
    total_tokens = chat_completion.usage.total_tokens
    print(
        f"Completion time: {completion_time}, Prompt Tokens: {prompt_tokens}, Completion Tokens: {completion_tokens}, Total tokens: {total_tokens}"
    )
    print(response)

    return {
        "response": response,
        "completion_time": completion_time,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }


async def main():
    image_url = "https://cupcakesproteinshakes.wordpress.com/wp-content/uploads/2013/10/ingredients.jpg"
    nutrition_info = await get_nutrition_info(image_url)
    print(type(nutrition_info))


if __name__ == "__main__":
    asyncio.run(main())
