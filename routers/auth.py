from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.get("/hello_faxa/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
