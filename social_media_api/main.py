import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI

from social_media_api.database import database
from social_media_api.logging_conf import configure_logging
from social_media_api.routers.post import router as post_router


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Logging configured")
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(post_router)
