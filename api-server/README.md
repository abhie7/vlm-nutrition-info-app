# FastAPI API Server

This project is a FastAPI-based API server designed to handle image uploads, process them, and interact with a large language model (LLM) via an external API. The server follows the MVC architecture and utilizes MongoDB for data storage.

## Project Structure

```
fastapi-api-server
├── app
│   ├── api
│   │   ├── endpoints
│   │   │   └── image.py
│   │   └── __init__.py
│   ├── core
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── __init__.py
│   ├── models
│   │   ├── image.py
│   │   └── __init__.py
│   ├── services
│   │   ├── image_service.py
│   │   └── __init__.py
│   ├── main.py
│   └── __init__.py
├── logs
│   └── app.log
├── requirements.txt
├── README.md
└── .env
```

## Features

- **Image Upload**: Users can upload images through the API.
- **LLM Integration**: The server sends the image URL to an LLM API and returns the response to the user.
- **Asynchronous Processing**: All routes are designed to be asynchronous for optimal performance.
- **MongoDB Storage**: All relevant data is stored in a MongoDB database.
- **Logging**: A global logger captures application events and errors, saving them with timestamps.

## Setup Instructions

1. **Clone the Repository**:

   ```
   git clone <repository-url>
   cd fastapi-api-server
   ```

2. **Create a Virtual Environment**:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your configuration settings, such as database connection details and API keys.

5. **Run the Application**:
   ```
   uvicorn app.main:app --reload
   ```

## API Endpoints

- **POST /upload-image**: Upload an image and receive a response from the LLM.

## Logging

Logs are stored in `logs/app.log`. Ensure that the application has write permissions to this directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

api-server
├───.env
├───main.py
├───app
│ ├───config
│ │ └───settings.py
│ ├───database
│ │ ├───image_analysis_repository.py
│ │ ├───user_repository.py
│ │ └───base_repository.py
│ ├───logs
│ ├───middlewares
│ │ └───logging_middleware.py
│ ├───models
│ │ ├───user.py
│ │ └───image_analysis.py
│ ├───routes
│ │ ├───auth.py
│ │ ├───endpoints.py
│ │ └───image.py
│ ├───services
│ │ ├───vlm_service.py
│ │ └───auth_service.py
│ ├───utils
│ │ └───get_password_hash.py

graph TD
    A[Start App] --> B[Landing Page]
    B --> C{User Status}
    C -->|New User| D[Signup Page]
    C -->|Existing User| E[Login Page]
    E -->|Forgot Password| F[Password Reset Page]
    
    D --> G[Create Account]
    G --> H[Dashboard]
    E --> I{Valid Credentials?}
    I -->|Yes| H
    I -->|No| E
    F --> J[Send Reset Email]
    J --> K[Set New Password]
    K --> E
    
    H --> L{User Action}
    
    L -->|Scan Food Label| M[Open Scan Modal]
    M --> N{Scan Method}
    N -->|Upload from Device| O[Select Image]
    N -->|Use Camera| P[Take Photo]
    O --> Q[Process Image]
    P --> Q
    Q --> R[Display Extracted Nutrition Data]
    R --> S[Add Meal Context Form]
    S --> T[Save to Food Log]
    T --> H
    
    L -->|View Dashboard| U[Dashboard Overview]
    U --> V[View Macro Breakdown]
    U --> W[View Calorie Progress]
    U --> X[View Meal Distribution]
    
    L -->|Check Calendar| Y[Calendar View]
    Y --> Z{Select Date?}
    Z -->|Yes| AA[Show Day Details]
    Z -->|No| Y
    AA --> H
    
    L -->|View Nutrition Details| AB[Nutrition Details Panel]
    AB --> AC[Expand/Collapse Cards]
    AC --> AD[View Complete Nutritional Breakdown]
    AD --> H
    
    L -->|Track Water| AE[Water Intake Tracker]
    AE --> AF[Update Water Intake]
    AF --> AG[View Progress Toward Goal]
    AG --> H
    

I am building a VLM based app using React + Next.js with Vite and TypeScript with ShadCN/UI and AceternityUI, TailwindCSS, ReduxToolkit based frontend and FastAPI, MongoDB, Groq based backend.

The users can upload the picture of the nutritional info about a product/food label and I will use a VLM to extract all the needed info - calories, proteins, etc. and save it in the user's mongo collection. how is this? Then the user can track and view their daily intake in a dynamic user friendly dashboard format with all the necessary filters, charts, graphs, etc.

now for the frontend please help me decide the flow and what all I should display by creating a complete beautiful modern UI.

here are my base requirements:

- I want to create it using ReactJS + NextJS with ShadCN/ui and TailwindCSS, Redux Toolkit for state management,
- Backend is created using FastAPIs so everything will be REST API based, no need for express server.
- Login / Signup/ Forgot Password pages with authentication - create the user_uuid and save user in mongo User collection with email, password, user_uuid, display_name, created_at, last_login from the backend
- Robust Sidebar from Shadcn
- Upload Label / give a better term - Button which opens a dialog and the user has 2 options - Upload from device or click a pic (opens camera)
- after selecting pic, give a form:
  - food_display_name,
  - meal_type: color coded - breakfast, lunch, dinner, snack, binge
  - tags: color coded tags - select one or many (sweet, spicy, healthy, fatty, etc.)
- after the user inputs and clicks Analyze button, send these data in the payload to the backend using a post request.
- the backend will analyse using VLM and send the response.
- Show a loader until then and display creative messages - "Have a glass of water", "This usually is pretty quick, i dont know what happened", positive messages
- after that route the user to the dashboard where they can see all the charts and graphs.
- display all the possible graphs and charts with filter with everything option.
- from the sidebar, there should be a calendar route, in the calendar page, users will view a calendar with daily intake of food, with filter \* by default display calories but user can view protein or any other nutrient(s)
- what else can I add to this tracker? daily water intake?
- Drag and drop support
- Mobile camera integration

this is how i am storing nutrition_info data in my current db

```
{
  "_id": {
    "$oid": "67c8731941018648e99de87c"
  },
  "user_uuid": "1234",
  "food_name": "kurkure",
  "meal_type": "snack",
  "request_id": "f77e1910-6963-46a9-bfbc-74140273ade8",
  "tags": [
    "spicy",
    "salty",
    "fatty"
  ],
  "image_url": "https://www.pediasure.com/child-development-nutrition/nutrition-facts-kids/_jcr_content/root/container/columncontrol/tab_item_no_1/image.coreimg.85.1024.jpeg/1719295141553/pds-22-0802901-img-pediasure-how-to-read-nutrition-labels-new25.jpeg",
  "nutrient_info": {
    "metadata": {
      "confidence_score": 0.99,
      "error_status": false
    },
    "product_details": {
      "serving_size": {
        "amount": 237,
        "unit": "ml",
        "type": "container"
      }
    },
    "total_calories": 240,
    "nutrients": {
      "total_fat": {
        "amount": 9,
        "unit": "g",
        "daily_value_percentage": 12,
        "group": "fats",
        "category": "macronutrient",
        "sub_nutrients": {
          "saturated_fat": {
            "amount": 1,
            "unit": "g",
            "daily_value_percentage": 5,
            "group": "fats",
            "category": "macronutrient"
          },
          "trans_fat": {
            "amount": 0,
            "unit": "g",
            "daily_value_percentage": 0,
            "group": "fats",
            "category": "macronutrient"
          }
        }
      },
      "cholesterol": {
        "amount": 5,
        "unit": "mg",
        "daily_value_percentage": "<2%",
        "group": "fats",
        "category": "macronutrient"
      },
      "carbohydrates": {
        "amount": 90,
        "unit": "mg",
        "daily_value_percentage": 12,
        "group": "carbohydrates",
        "category": "macronutrient",
        "sub_nutrients": {
          "dietary_fiber": {
            "amount": 1,
            "unit": "g",
            "daily_value_percentage": "<2%",
            "group": "carbohydrates",
            "category": "macronutrient"
          },
          "total_sugars": {
            "amount": 12,
            "unit": "g",
            "daily_value_percentage": 22,
            "group": "carbohydrates",
            "category": "macronutrient"
          },
          "added_sugars": {
            "amount": 11,
            "unit": "g",
            "daily_value_percentage": 22,
            "group": "carbohydrates",
            "category": "macronutrient"
          }
        }
      },
      "protein": {
        "amount": 7,
        "unit": "g",
        "daily_value_percentage": 14,
        "group": "protein",
        "category": "macronutrient"
      },
      "sodium": {
        "amount": 90,
        "unit": "mg",
        "daily_value_percentage": 4,
        "group": "mineral",
        "category": "micronutrient"
      },
      "calcium": {
        "amount": 330,
        "unit": "mg",
        "daily_value_percentage": 25,
        "group": "mineral",
        "category": "micronutrient"
      },
      "iron": {
        "amount": 2.7,
        "unit": "mg",
        "daily_value_percentage": 15,
        "group": "mineral",
        "category": "micronutrient"
      },
      "vitamins": [
        {
          "vitamin_type": "A",
          "amount": 15,
          "unit": "mcg",
          "daily_value_percentage": 25,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "C",
          "amount": 25,
          "unit": "mg",
          "daily_value_percentage": 25,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "E",
          "amount": 20,
          "unit": "mg",
          "daily_value_percentage": 20,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "K",
          "amount": 15,
          "unit": "mcg",
          "daily_value_percentage": 15,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "B2",
          "amount": 20,
          "unit": "mg",
          "daily_value_percentage": 25,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "B3",
          "amount": 20,
          "unit": "mg",
          "daily_value_percentage": 25,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "B5",
          "amount": 25,
          "unit": "mg",
          "daily_value_percentage": 25,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "B6",
          "amount": 20,
          "unit": "mg",
          "daily_value_percentage": 25,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "B12",
          "amount": 25,
          "unit": "mcg",
          "daily_value_percentage": 25,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "Biotin",
          "amount": 25,
          "unit": "mcg",
          "daily_value_percentage": 25,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "Folic Acid",
          "amount": 25,
          "unit": "mcg",
          "daily_value_percentage": 25,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "Phosphorus",
          "amount": 20,
          "unit": "mg",
          "daily_value_percentage": 20,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "Iodine",
          "amount": 15,
          "unit": "mcg",
          "daily_value_percentage": 15,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "Magnesium",
          "amount": 10,
          "unit": "mg",
          "daily_value_percentage": 25,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "Zinc",
          "amount": 15,
          "unit": "mg",
          "daily_value_percentage": 15,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "Selenium",
          "amount": 15,
          "unit": "mcg",
          "daily_value_percentage": 20,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "Copper",
          "amount": 15,
          "unit": "mg",
          "daily_value_percentage": 15,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "Manganese",
          "amount": 20,
          "unit": "mg",
          "daily_value_percentage": 20,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "Chromium",
          "amount": 25,
          "unit": "mcg",
          "daily_value_percentage": 20,
          "group": "vitamins",
          "category": "micronutrient"
        },
        {
          "vitamin_type": "Molybdenum",
          "amount": 20,
          "unit": "mcg",
          "daily_value_percentage": 20,
          "group": "vitamins",
          "category": "micronutrient"
        }
      ]
    }
  },
  "token_usage": {
    "prompt_tokens": 1044,
    "completion_tokens": 7149,
    "total_tokens": 8193
  },
  "created_at": {
    "$date": "2025-03-05T21:21:53.732Z"
  },
  "status": "completed",
  "vlm_response_time": 10.15,
  "processing_time": 11.275063
}
```

PLEASE MAKE SURE THAT THIS HAS DARK MODE SELECTOR, MULTIPLE COLOR THEMES, AND IS RESPONSIVE AND COMPATIBLE WITH MOBILES.

PRD:

NutriScan: AI-Powered Nutrition Tracking App

NutriScan is a modern nutrition tracking application that uses vision language models to extract nutritional information from food labels, allowing users to effortlessly track their daily intake through an intuitive dashboard with comprehensive analytics. This is completely responsive for mobile apps.

- Amazing and beautiful and modern Login/Signup/Forgot Password pages with infor about the app
- Upload & Scan Interface - Clean, minimalist design with a prominent "Scan Label" button that opens a modal with options to upload from device or use camera, followed by a form to add meal context
- Dashboard Overview - Feature-rich dashboard with macro/micronutrient breakdowns, daily calorie targets, and meal distribution in visually appealing charts (donut, bar, line graphs)
- Calendar View - Interactive calendar showing daily nutrition patterns with color-coded indicators for meeting targets and detailed day view on selection
- Nutrition Details Panel - Expandable cards showing comprehensive breakdown of scanned items with all extracted nutritional data in an organized, visually appealing format
- Water Intake Tracker - Simple, visual water tracking component with animated fill indicators and daily goal setting
