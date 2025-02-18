from fastapi import FastAPI
from app.routers import chat
from app.database.api import init_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(chat.router)


@app.get("/")
async def home():
    return {"message": "AI Chat API is running!"}
