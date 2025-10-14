import os
import sys 
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), "api"))

# Initialize centralized logging FIRST before any other imports
from common.utils.logger import setup_logging
setup_logging(log_level="INFO")  # Change to "INFO" for production

from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 

from api.database_apis import db_router  # type: ignore
from api.workflow_apis import workflow_router  # type: ignore
from api.browser_auto_apis import browser_router  # type: ignore
from api.test_apis import test_apis
from kogoos_common.util.config import get_settings

from dotenv import load_dotenv
load_dotenv(".env")  # Load .env file into environment 

logger = logging.getLogger(__name__)

logger.info("=" * 80)
logger.info("🚀 Starting Browsey Server Application")
logger.info("=" * 80)

logger.info("📋 Loading settings...")
try:
    settings = get_settings()
    prefix = f"{settings.API_PREF_STR}/browsey"
    logger.info("✓ Settings loaded successfully")
    logger.info(f"📍 API Prefix: {prefix}")
except Exception as e:
    logger.error(f"❌ Error getting settings: {e}")
    import traceback
    logger.error(traceback.format_exc())
    raise

app = FastAPI() 

# Add CORS middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Replace with your frontend's URL 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods 
    allow_headers=["*"],  # Allow all headers
) 


# Group all routes under the main prefix
app.include_router(db_router, prefix=prefix)
app.include_router(workflow_router, prefix=prefix)
app.include_router(browser_router, prefix=prefix)
app.include_router(test_apis, prefix=prefix)




if __name__ == "__main__":
    host = os.getenv("API_URL_IP", "0.0.0.0")
    port = 5010
    logger.info("=" * 80)
    logger.info(f"🌐 Starting Uvicorn server on {host}:{port}")
    logger.info("=" * 80)
    uvicorn.run("main:app", host=host, port=port) 


