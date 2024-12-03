import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time
from typing import List, Dict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WellfoundScraper:
    BASE_URL = "https://wellfound.com/jobs"
    
    def __init__(self):
        self.driver = None
    
    def create_driver(self):
        try:
            options = uc.ChromeOptions()
            # Essential headless mode settings
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Create driver in headless mode
            driver = uc.Chrome(
                options=options,
                headless=True,  # Ensure headless mode is enabled
                use_subprocess=True  # Use subprocess to prevent window opening
            )
            
            return driver
        except Exception as e:
            logging.error(f"Error creating Chrome WebDriver: {str(e)}")
            raise
    
    def scrape_jobs_for_keyword(self, keyword: str, max_jobs: int = 10) -> List[Dict]:
        try:
            if not self.driver:
                self.driver = self.create_driver()
            
            search_url = f"{self.BASE_URL}/search?q={keyword}&remote=true"
            logging.info(f"Accessing: {search_url}")
            
            self.driver.get(search_url)
            time.sleep(5)
            
            # Scroll to load more content
            self.driver.execute_script("""
                window.scrollTo(0, document.body.scrollHeight);
                return document.body.scrollHeight;
            """)
            time.sleep(2)
            
            # Updated selectors for job cards
            job_cards = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-test='StartupResult']"))
            )
            
            jobs = []
            for card in job_cards[:max_jobs]:
                try:
                    # Extract job details
                    title = card.find_element(By.CSS_SELECTOR, "h2, div[role='heading']").text.strip()
                    company = card.find_element(By.CSS_SELECTOR, "a.content-center, div[class*='styles_component_dBLcB']").text.strip()
                    location = card.find_element(By.CSS_SELECTOR, "div[class*='styles_component_Z5tpa']").text.strip()
                    
                    # Get the job link
                    job_link = card.find_element(By.CSS_SELECTOR, "a[href*='/jobs/']").get_attribute("href")
                    
                    # Try to get salary and posted date
                    try:
                        salary = card.find_element(By.CSS_SELECTOR, "div[contains(text(),'₹')]").text.strip()
                    except:
                        salary = "Salary not specified"
                    
                    try:
                        posted_date = card.find_element(By.CSS_SELECTOR, "div[contains(text(),'POSTED')]").text.strip()
                    except:
                        posted_date = "Recently posted"
                    
                    job_data = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "salary": salary,
                        "posted_date": posted_date,
                        "job_link": job_link,
                        "keyword": keyword
                    }
                    
                    jobs.append(job_data)
                    logging.info(f"Scraped job: {title} at {company}")
                    
                except Exception as e:
                    logging.error(f"Error extracting job details: {str(e)}")
                    continue
            
            return jobs
            
        except Exception as e:
            logging.error(f"Error scraping jobs for keyword {keyword}: {str(e)}")
            return []
        
    def scrape_jobs(self, keywords: List[str], max_jobs_per_keyword: int = 10) -> List[Dict]:
        all_jobs = []
        try:
            for keyword in keywords:
                jobs = self.scrape_jobs_for_keyword(keyword, max_jobs_per_keyword)
                all_jobs.extend(jobs)
            return all_jobs
        except Exception as e:
            logging.error(f"Error in scrape_jobs: {str(e)}")
            return all_jobs
        finally:
            self.close()
    
    def close(self):
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                logging.info("WebDriver closed successfully")
        except Exception as e:
            logging.error(f"Error closing WebDriver: {str(e)}")

if __name__ == "__main__":
    # Test the scraper
    scraper = WellfoundScraper()
    jobs = scraper.scrape_jobs(["python developer"], max_jobs_per_keyword=5)
    print(f"Found {len(jobs)} jobs")
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print("---")