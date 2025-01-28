from contextlib import asynccontextmanager

from fastapi import FastAPI

from models.database import db
from routers import auth_router, admin_router


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await db.create_all()
    # app_.include_router(auth_router)
    app_.include_router(admin_router)
    yield

app = FastAPI(lifespan=lifespan)


