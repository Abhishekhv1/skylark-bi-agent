# Monday.com Business Intelligence Agent

A full-stack, AI-powered Business Intelligence agent designed to query, synthesize, and analyze live deal pipelines and operational work orders from Monday.com. Built as a prototype for Skylark Drones.

## Live Demo
* **Frontend UI (Vercel):** [Insert your Vercel URL here]
* **Backend API (Render):** [Insert your Render URL here]

## Tech Stack
* **Frontend:** React, Vite, CSS, React-Markdown, Remark-GFM
* **Backend:** Python, FastAPI, Uvicorn, Pandas
* **Integrations:** Monday.com GraphQL API, Google Gemini AI API

## Core Features
* **Cross-Board Intelligence:** Simultaneously pulls and synthesizes data from both Sales Pipeline (Deals) and Project Execution (Work Orders) boards.
* **Data Resilience:** Built-in Pandas logic handles edge cases, missing data, and 'Unknown' statuses without breaking the application.
* **Executive Formatting:** Uses GitHub Flavored Markdown to render clean, readable tables and lists in the chat UI.
* **Fully Asynchronous:** Built on FastAPI to ensure rapid, non-blocking requests to external APIs.

## Local Setup Instructions

If you wish to run this project locally, follow the steps below.

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/YOUR_USERNAME/skylark-bi-agent.git
cd skylark-bi-agent
\`\`\`

### 2. Environment Variables
Create a `.env` file in the root directory and add your specific API keys and Board IDs:
\`\`\`env
MONDAY_API_TOKEN=your_monday_token_here
DEALS_BOARD_ID=your_deals_board_id_here
WORK_ORDERS_BOARD_ID=your_work_orders_board_id_here
GEMINI_API_KEY=your_gemini_api_key_here
\`\`\`

### 3. Backend Setup
Make sure you have Python 3.8+ installed. From the root directory:
\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload
\`\`\`
The backend will run on `http://127.0.0.1:8000`.

### 4. Frontend Setup
Open a new terminal window.
\`\`\`bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
\`\`\`
The frontend will run on `http://localhost:5173/`. 

*(Note: For local development, ensure the fetch URL in `frontend/src/App.jsx` points to `http://127.0.0.1:8000/api/chat` instead of the live Render URL).*