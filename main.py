from contextlib import asynccontextmanager

from fastapi import FastAPI

from models import db
from routers import auth_router


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await db.create_all()
    app_.include_router(auth_router)
    yield


app = FastAPI(lifespan=lifespan)
