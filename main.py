from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from monday_service import get_clean_deals_data, get_clean_work_orders_data
from agent import query_agent

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin (e.g., http://localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Allows all HTTP headers
)

class ChatRequest(BaseModel):
    message: str

@app.get("/api/deals")
def get_deals():
    df = get_clean_deals_data()
    return {"data": df.to_dict(orient="records")}

@app.get("/api/work-orders")
def get_work_orders():
    df = get_clean_work_orders_data()
    return {"data": df.to_dict(orient="records")}

@app.post("/api/chat")
def chat_with_agent(request: ChatRequest):
    agent_response = query_agent(request.message)
    return {"response": agent_response}