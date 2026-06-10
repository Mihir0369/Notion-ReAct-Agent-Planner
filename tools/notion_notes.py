import os
import requests
from langchain.tools import tool


@tool
def get_notion_notes() -> list:
    """Get all the pending notes from Notion"""

    api_key = os.getenv("NOTION_API_KEY")
    db_id = os.getenv("NOTION_NOTES_DB_ID")

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
            "property": "Status",
            "select": {
                "equals": "Pending",
            },
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        notes = []
        for result in data.get("results", []):
            props = result.get("properties", {})
            title_list = props.get("Note", {}).get("title", [])
            note_content = title_list[0].get("text", {}).get("content", "") if title_list else "Untitle Note"
            notes.append(note_content)
        return notes

    except Exception as e:
        return [f"error :  Error fetching notes: {e}"]

@tool
def add_notion_note(note: str) -> str:
    """Add a new note to Notion"""

    api_key = os.getenv("NOTION_API_KEY")
    db_id = os.getenv("NOTION_NOTES_DB_ID")

    if not api_key or not db_id:
        return {"error" : "Notion API key or database ID not found"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {
            "database_id": db_id,
        },
        "properties": {
            "Note": {
                "title": [{"text": {"content": note}}]
            },
            "Status": {
                "select": {"name": "Pending"}
            }
    }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return f"Note added successfully: {note}"

    except Exception as e:
        return f"error : Error adding note: {e}"