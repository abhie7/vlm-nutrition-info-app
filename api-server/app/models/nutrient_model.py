from typing import Any, List, Optional, Union, Dict
from enum import Enum
from pydantic import BaseModel


class NutrientCategory(str, Enum):
    MACRONUTRIENT = "macronutrient"
    MICRONUTRIENT = "micronutrient"
    MINERAL = "mineral"
    VITAMIN = "vitamin"


class NutrientGroup(str, Enum):
    FATS = "fats"
    CARBOHYDRATES = "carbohydrates"
    PROTEIN = "protein"
    ELECTROLYTES = "electrolytes"


class ServingType(str, Enum):
    CALORIES = "calories"
    SERVING = "serving"
    CONTAINER = "container"


class NutrientSchema(BaseModel):
    # Core Nutrient Attributes
    name: str  # Standardized name for easy graphing
    display_name: Optional[str] = None  # User-friendly name
    amount: float
    unit: str

    # Categorization Attributes
    category: Optional[NutrientCategory] = None
    group: Optional[NutrientGroup] = None

    # Nutritional Context
    daily_value_percentage: Optional[float] = None
    type: Optional[str] = None  # Additional type information

    # Visualization Attributes
    color_code: Optional[str] = None  # Hex color for graphs
    display_priority: int = 0  # For sorting in visualizations

    # Optional Sub-Nutrients (for complex nutrients)
    sub_nutrients: Optional[List["NutrientSchema"]] = None


class NutritionLabel(BaseModel):
    metadata: Dict[str, Union[float, bool, str]] = {
        "confidence_score": 0.0,
        "error_status": False,
        "processed_timestamp": None,
    }

    product_details: Dict[str, Any] = {
        "serving_size": {"amount": 0.0, "unit": "g", "type": ServingType.SERVING}
    }

    # Comprehensive Nutrients Array with Predefined Structure
    nutrients: List[NutrientSchema] = [
        # Macronutrients (always present, even if 0)
        NutrientSchema(
            name="total_fat",
            display_name="Total Fat",
            amount=0.0,
            unit="g",
            category=NutrientCategory.MACRONUTRIENT,
            group=NutrientGroup.FATS,
            color_code="#FF6384",
            display_priority=1,
            sub_nutrients=[
                NutrientSchema(
                    name="saturated_fat",
                    display_name="Saturated Fat",
                    amount=0.0,
                    unit="g",
                    category=NutrientCategory.MACRONUTRIENT,
                    group=NutrientGroup.FATS,
                    color_code="#36A2EB",
                ),
                NutrientSchema(
                    name="trans_fat",
                    display_name="Trans Fat",
                    amount=0.0,
                    unit="g",
                    category=NutrientCategory.MACRONUTRIENT,
                    group=NutrientGroup.FATS,
                    color_code="#FFCE56",
                ),
            ],
        ),
        NutrientSchema(
            name="carbohydrates",
            display_name="Total Carbohydrates",
            amount=0.0,
            unit="g",
            category=NutrientCategory.MACRONUTRIENT,
            group=NutrientGroup.CARBOHYDRATES,
            color_code="#4BC0C0",
            display_priority=2,
            sub_nutrients=[
                NutrientSchema(
                    name="fiber",
                    display_name="Dietary Fiber",
                    amount=0.0,
                    unit="g",
                    category=NutrientCategory.MACRONUTRIENT,
                    group=NutrientGroup.CARBOHYDRATES,
                    color_code="#9966FF",
                ),
                NutrientSchema(
                    name="total_sugar",
                    display_name="Total Sugars",
                    amount=0.0,
                    unit="g",
                    category=NutrientCategory.MACRONUTRIENT,
                    group=NutrientGroup.CARBOHYDRATES,
                    color_code="#FF9F40",
                ),
                NutrientSchema(
                    name="added_sugar",
                    display_name="Added Sugars",
                    amount=0.0,
                    unit="g",
                    category=NutrientCategory.MACRONUTRIENT,
                    group=NutrientGroup.CARBOHYDRATES,
                    color_code="#FFCD94",
                ),
            ],
        ),
        NutrientSchema(
            name="protein",
            display_name="Protein",
            amount=0.0,
            unit="g",
            category=NutrientCategory.MACRONUTRIENT,
            group=NutrientGroup.PROTEIN,
            color_code="#00A86B",
            display_priority=3,
        ),
    ]

    # Predefined Micronutrients with Visualization Support
    micronutrients: List[NutrientSchema] = [
        # Minerals
        NutrientSchema(
            name="sodium",
            display_name="Sodium",
            amount=0.0,
            unit="mg",
            category=NutrientCategory.MINERAL,
            group=NutrientGroup.ELECTROLYTES,
            color_code="#FF6384",
        ),
        NutrientSchema(
            name="calcium",
            display_name="Calcium",
            amount=0.0,
            unit="mg",
            category=NutrientCategory.MINERAL,
            color_code="#36A2EB",
        ),
        NutrientSchema(
            name="iron",
            display_name="Iron",
            amount=0.0,
            unit="mg",
            category=NutrientCategory.MINERAL,
            color_code="#FFCE56",
        ),
        # Vitamins (with predefined vitamin types)
        NutrientSchema(
            name="vitamin_a",
            display_name="Vitamin A",
            amount=0.0,
            unit="mcg",
            category=NutrientCategory.VITAMIN,
            color_code="#4BC0C0",
        ),
        NutrientSchema(
            name="vitamin_c",
            display_name="Vitamin C",
            amount=0.0,
            unit="mg",
            category=NutrientCategory.VITAMIN,
            color_code="#9966FF",
        ),
    ]

    total_calories: int = 0
    ingredients: Optional[List[str]] = None
    allergens: Optional[List[str]] = None


# Example of how to use and extend
def create_nutrition_label(data: dict) -> NutritionLabel:
    # Flexible creation with automatic mapping
    label = NutritionLabel()

    # Intelligent mapping of input data
    for nutrient in label.nutrients:
        if nutrient.name in data:
            nutrient.amount = data.get(nutrient.name, 0.0)

    # Similar logic for micronutrients
    for micronutrient in label.micronutrients:
        if micronutrient.name in data:
            micronutrient.amount = data.get(micronutrient.name, 0.0)

    return label


# Example Usage
example_data = {
    "total_fat": 10.5,
    "saturated_fat": 3.2,
    "carbohydrates": 25.0,
    "fiber": 2.5,
    "protein": 15.0,
    "sodium": 250,
    "vitamin_c": 15.0,
}

nutrition_label = create_nutrition_label(example_data)
