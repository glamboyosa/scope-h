from fastapi import FastAPI
from src.scraper import Scraper

app = FastAPI()

scraper = Scraper()

@app.get("/")
async def root():
    return {"message": "Hello World"}
