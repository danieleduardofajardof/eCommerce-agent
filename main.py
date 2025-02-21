from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str


# Load environment variables from .env file
load_dotenv()

# Retrieve API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Mock product catalog
PRODUCT_CATALOG = [
    {"id": 1, "name": "EcoFriendly Water Bottle", "description": "A reusable water bottle made from recycled materials.", "price": 15.99, "stock": 10},
    {"id": 2, "name": "Wireless Headphones", "description": "Noise-canceling over-ear headphones with long battery life.", "price": 99.99, "stock": 5},
    {"id": 3, "name": "Smartwatch", "description": "A smartwatch with fitness tracking and notifications.", "price": 199.99, "stock": 2},
    {"id": 4, "name": "Gaming Mouse", "description": "Ergonomic gaming mouse with customizable buttons.", "price": 49.99, "stock": 8},
    {"id": 5, "name": "Mechanical Keyboard", "description": "High-quality mechanical keyboard with RGB lighting.", "price": 129.99, "stock": 3}
]

# Function to retrieve product info
def get_product_info(product_name):
    for product in PRODUCT_CATALOG:
        if product["name"].lower() == product_name.lower():
            return product
    return {"error": "Product not found"}

# Function to check stock availability
def check_stock(product_name):
    for product in PRODUCT_CATALOG:
        if product["name"].lower() == product_name.lower():
            return {"name": product["name"], "stock": product["stock"]}
    return {"error": "Product not found"}

# OpenAI function calling setup
client = OpenAI(api_key=OPENAI_API_KEY)


functions = [
    {
        "type": "function",
        "function":{
        "name": "get_product_info",
        "description": "Get details about a product",
        "parameters": {
            "type": "object",
            "properties": {
                "productName": {"type": "string"}
            },
            "required": ["productName"]
        }}
    },
    {
        "type": "function",   "function":{
        "name": "check_stock",
        "description": "Check stock availability of a product",
        "parameters": {
            "type": "object",
            "properties": {
                "productName": {"type": "string"}
            },
            "required": ["productName"]
        }
    }}
]

# Create Assistant
assistant = client.beta.assistants.create(
    name="ShopBot",
    instructions="You are an AI assistant for an e-commerce store. You help customers with product information and availability.",
    model="gpt-4o",
    tools=functions
)

# Chat function
def chat_with_assistant(user_input):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_input}],
        tools=functions
    )
    if response.choices and response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]

        # Extract function name & arguments
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        # Step 3: Execute the function
        if ((function_name == "get_product_info" )| (function_name == "check_stock")):
            product_info = get_product_info(function_args["productName"])

            # Step 4: Send the function result back to OpenAI for a response
            final_response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Tell me about the EcoFriendly Water Bottle."},
                {"role": "assistant", "tool_calls": [tool_call]},
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,  # ✅ REQUIRED FIX: Include tool_call_id
                    "name": function_name,
                    "content": json.dumps(product_info)
                }
            ]
        )
            return final_response

@app.post("/chat/")


def chat_endpoint(request: dict):
    user_input = request.get("message")
    if not user_input:
        raise HTTPException(status_code=400, detail="Message is required")
    response = chat_with_assistant(user_input)
    print(response)
    print(response.choices[0].message.content)  # ✅ Correct way to access the assistant's response

    return {"response": response.choices[0].message.content}
