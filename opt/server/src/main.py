from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.scraper import Scraper

import threading

app = FastAPI()

scraper = Scraper()

task_statuses = {}
task_df = {}
def background_task(task_id):
    ig_influencers_df = scraper.get_ig_users_info_for_brand()
    grouped_df = scraper.group_by_ig_username(ig_influencers_df)
    _, result = scraper.add_influencer_score_columns(*grouped_df)
    print(result)
    task_df[task_id] = result
    task_statuses[task_id] = "completed"
    print("Background task complete")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    
    return {"message": "Hello World"}

@app.get("/background-task/{task_id}/") 
async def handler(task_id: int):
    if task_id in task_statuses and task_statuses[task_id] == "completed": 
        return {"data": task_df[task_id], "status": task_statuses[task_id] }
    else: 
        return {"data": None, "status": task_statuses[task_id]}

@app.post("/background-task/")
async def handler():
    task_id = threading.get_ident()  # Get the unique thread identifier
    task_statuses[task_id] = "processing"
    print(task_id)
    def run_task():
        background_task(task_id)

    # Create and start a new thread for the background task
    background_thread = threading.Thread(target=run_task)
    background_thread.start()

    return {"task_id": task_id, "status": "started"}
