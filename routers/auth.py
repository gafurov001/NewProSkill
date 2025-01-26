from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.get("/hello_faxa4/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
