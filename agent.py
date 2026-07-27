import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from monday_service import get_clean_deals_data, get_clean_work_orders_data

load_dotenv()

# Initialize the Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define the Tools
def get_sales_pipeline_data() -> str:
    """
    Fetches the current sales pipeline and deal data. 
    Use this when the user asks about revenue, deals, sales, pipeline health, or closing dates.
    """
    df = get_clean_deals_data()
    return df.to_json(orient="records")

def get_work_order_status() -> str:
    """
    Fetches current project execution and work order data.
    Use this when the user asks about project statuses, operations, execution, or deliverables.
    """
    df = get_clean_work_orders_data()
    return df.to_json(orient="records")

# Define the Persona
SYSTEM_PROMPT = """
You are an expert Business Intelligence AI Agent for executives. 
Your job is to answer founder-level business questions using the provided tools.

Guidelines:
1. Always analyze the data provided by your tools carefully before answering.
2. If data is missing or marked as 'Unknown', state this caveat clearly.
3. Provide context and insights, not just raw numbers or data dumps.
4. If a query is too vague (e.g., "How are we doing?"), ask a clarifying question.
"""

def query_agent(user_message: str) -> str:
    """
    Sends the user query to Gemini, allowing it to automatically call 
    the necessary tools and return a synthesized response.
    """
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[get_sales_pipeline_data, get_work_order_status],
            temperature=0.2, # Low temperature for more analytical, factual responses
        ),
    )
    
    return response.text