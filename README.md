### eCommerce-Agent

## Overview

This project is an AI-powered eCommerce chatbot that provides product information and checks stock availability. It integrates with OpenAI's API using function calling to handle user queries efficiently.

# Features

Retrieves product details

Checks stock availability

Uses OpenAI function calling

FastAPI backend for API handling

# Technologies Used

Python

FastAPI

OpenAI API

dotenv

JSON

Git

# Setup Instructions

1. Clone the Repository

git clone https://github.com/danieleduardofajardof/eCommerce-agent.git
cd eCommerce-agent

2. Install Dependencies

Ensure you have Python installed, then run:

pip install -r requirements.txt

3. Set Up Environment Variables

Create a .env file and add your OpenAI API key:

OPENAI_API_KEY=your_api_key_here

4. Run the FastAPI Server

uvicorn main:app --reload

5. Test the API

Use the /chat/ endpoint to communicate with the chatbot:

{
  "message": "Tell me about the EcoFriendly Water Bottle."
}

API Endpoints

POST /chat/

Request Body:

{
  "message": "<User Query>"
}

Response:

{
  "response": "<Bot's Response>"
}

Deployment

Build a Docker image:

docker build -t ecommerce-agent .

Run the container:

docker run -p 8000:8000 --env-file .env ecommerce-agent

Excluding .env from Git

Ensure your .env file is not committed by adding it to .gitignore:

.env

# License

MIT License

This project is open-source. Contributions are welcome!

