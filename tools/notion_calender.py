import os
import requests
from langchain.tools import tool

@tool
def get_calender_events(date: str) -> dict:
    """Get the events from the calender for a given date (YYYY-MM-DD) from Notion.
    """
    api_key = os.getenv("NOTION_API_KEY")
    db_id = os.getenv("NOTION_CALENDAR_DB_ID")

    if not api_key or not db_id:
        return {"error" : "Notion API key or database ID not found"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    url = f"https://api.notion.com/v1/databases/{db_id}/query"

    payload = {
        "filter": {
            "property": "Date",
            "date": {
                "equals": date,
            },
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        events = []
        for result in data.get("results", []):
            props = result.get("properties", {})    
            title_list = props.get("Event", {}).get("title", [])
            event_name = title_list[0].get("text", {}).get("content", "") if title_list else "Untitled Event"

            time_list = props.get("Time", {}).get("rich_text", [])
            event_time = time_list[0].get("text", {}).get("content", "") if time_list else "All Day"
            events.append(
                {
                "event":event_name,
                "time": event_time
                }
            )
        return {"events": events, "date": date}

    except Exception as e:  
        return {f"error : Error fetching events: {e}"}

@tool
def add_calender_event(event: str, date: str, time: str) -> str:
    """Add a new event to the calender in the notion.
    You have to provide event name, date and time.
    """
    api_key = os.getenv("NOTION_API_KEY")
    db_id = os.getenv("NOTION_CALENDAR_DB_ID")
    
    if not api_key or not db_id:
        return {"error" : "Notion API key or database ID not found"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    url = "https://api.notion.com/v1/pages" 

    start_datetime = f"{date}T{time}:00" if time else date

    payload = {
        "parent": {
            "database_id": db_id,
        },
        "properties": {
            "Event": {
                "title": [{"text": {"content": event}}]
            },
            "Date": {
                "date": {
                    "start": start_datetime,
                }
            },
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return f"Event added successfully: {event}"

    except Exception as e:
        return f"error : Error adding event: {e}"