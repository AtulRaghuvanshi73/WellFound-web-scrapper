from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from scraper import WellfoundScraper
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="Wellfound Job Scraper")

# CORS configuration to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobSearchRequest(BaseModel):
    keywords: List[str]
    max_jobs_per_keyword: int = 10

@app.post("/scrape-jobs")
async def scrape_jobs(request: JobSearchRequest):
    scraper = None
    try:
        logging.info(f"Received search request for keywords: {request.keywords}")
        
        if not request.keywords:
            raise HTTPException(status_code=400, detail="No keywords provided")
            
        scraper = WellfoundScraper()
        jobs = scraper.scrape_jobs(request.keywords, request.max_jobs_per_keyword)
        
        if not jobs:
            logging.warning("No jobs found for the given keywords")
            return {
                "status": "success",
                "jobs": [],
                "total_jobs": 0,
                "companies_by_keyword": {}
            }
        
        # Group companies by keyword
        companies_by_keyword = {}
        for job in jobs:
            keyword = job['keyword']
            if keyword not in companies_by_keyword:
                companies_by_keyword[keyword] = set()
            companies_by_keyword[keyword].add(job['company'])
        
        result = {
            "status": "success",
            "jobs": jobs,
            "total_jobs": len(jobs),
            "companies_by_keyword": {
                keyword: list(companies) 
                for keyword, companies in companies_by_keyword.items()
            }
        }
        
        logging.info(f"Successfully found {len(jobs)} jobs")
        return result
        
    except Exception as e:
        error_msg = f"Error during job scraping: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if scraper:
            try:
                scraper.close()
                logging.info("Scraper closed successfully")
            except Exception as e:
                logging.error(f"Error closing scraper: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Wellfound Job Scraper API"}