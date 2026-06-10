from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from agent.bot import make_agent
from utils.logger import get_logger
from tools.weather import get_weather
from tools.notion_notes import get_notion_notes, add_notion_note
from tools.notion_calender import get_calender_events, add_calender_event

logger = get_logger(__name__)

app = FastAPI(
    title="ReAct Agent Planner",
)

agent = None

@app.on_event("startup")
async def startup_event():
    global agent
    try:
        agent = make_agent()
        logger.info("Agent created successfully in API Server")
    except Exception as e:
        logger.error(f"Error creating agent in API Server: {e}")
        pass

class ChatRequest(BaseModel):
    messages: str
    history: Optional[List[Dict[str, Any]]] = None

@app.post("/chat")
async def chat(request: ChatRequest):
    global agent
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")

    try:
        response = agent.invoke({"messages": [("user", request.messages)]})
        if isinstance(response, dict) and "messages" in response:
            messages = response["messages"]
            if messages:
                last_msg = messages[-1]
                return {"response": last_msg.content}
    
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}