import os
import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_URL = "https://api.monday.com/v2"
HEADERS = {
    "Authorization": os.getenv("MONDAY_API_TOKEN"),
    "API-Version": "2024-04" 
}

def fetch_board_data(board_id):
    query = """
    query ($boardId: [ID!]) {
      boards(ids: $boardId) {
        items_page(limit: 500) {
          items {
            id
            name
            column_values {
              column {
                title
              }
              text
            }
          }
        }
      }
    }
    """
    
    variables = {"boardId": [board_id]}
    response = requests.post(
        MONDAY_API_URL, 
        json={"query": query, "variables": variables}, 
        headers=HEADERS
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.text}")

def clean_monday_data(json_data):
    items = json_data.get('data', {}).get('boards', [])[0].get('items_page', {}).get('items', [])
    
    parsed_data = []
    for item in items:
        row = {"Item Name": item.get("name")}
        for col in item.get("column_values", []):
            title = col.get("column", {}).get("title")
            val = col.get("text")
            row[title] = val
        parsed_data.append(row)
        
    df = pd.DataFrame(parsed_data)
    
    # 1. Convert empty strings to actual NaN values
    df.replace("", np.nan, inplace=True)
    
    # 2. Normalize column names (lowercase, replace spaces with underscores)
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    
# 3. Handle missing/null values gracefully
    df.fillna("Unknown", inplace=True)
    
    # 4. Dynamically force numeric conversion for financial/metric columns across BOTH boards
    for col in df.columns:
        if any(keyword in col for keyword in ['value', 'amount', 'masked', 'quantity']):
            # Replace 'Unknown' with 0 for math purposes, then force numeric conversion
            df[col] = pd.to_numeric(df[col].replace("Unknown", 0), errors='coerce').fillna(0)
            
    return df

def get_clean_deals_data():
    board_id = os.getenv("DEALS_BOARD_ID")
    raw_data = fetch_board_data(board_id)
    return clean_monday_data(raw_data)

def get_clean_work_orders_data():
    board_id = os.getenv("WORK_ORDERS_BOARD_ID")
    raw_data = fetch_board_data(board_id)
    return clean_monday_data(raw_data)