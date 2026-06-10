import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.agents import create_agent

from tools.weather import get_weather
from tools.notion_notes import get_notion_notes, add_notion_note
from tools.notion_calender import get_calender_events, add_calender_event
from utils.logger import get_logger

logger = get_logger(__name__)

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY not found")
        raise ValueError("GROQ_API_KEY not found")

    return ChatGroq(
        model_name="openai/gpt-oss-120b",
        temperature=0.5,
        api_key=api_key,
    )
    
def make_agent():
    logger.info("Creating agent")
    llm = get_llm()

    tools = [get_weather, get_notion_notes, add_notion_note, get_calender_events, add_calender_event]

    try:
        agent = create_agent(
            model=llm,
            tools=tools,
        )
        logger.info("Agent created successfully")
        return agent
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise e
    
