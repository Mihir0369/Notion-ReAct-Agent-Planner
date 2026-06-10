import uvicorn
from utils.logger import get_logger
from dotenv import load_dotenv
import os

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting API Server")
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)
    logger.info("API Server started successfully")