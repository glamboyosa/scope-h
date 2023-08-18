from fastapi import FastAPI
from src.scraper import Scraper



app = FastAPI()

scraper = Scraper()

@app.get("/")
async def root():
    ig_influencers_df = scraper.get_ig_users_info_for_brand()
    grouped_df = scraper.group_by_ig_username(ig_influencers_df)
    result = scraper.add_influencer_score_columns(*grouped_df)
    print(result)
    return {"message": "Hello World"}

@app.get("/scraper/") 
async def handler():
    return {}
