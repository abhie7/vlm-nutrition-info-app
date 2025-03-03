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