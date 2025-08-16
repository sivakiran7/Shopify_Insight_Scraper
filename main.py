from fastapi import FastAPI, Query, HTTPException # FastAPI → creates the API app.
# HTTPException → handles errors in a clean RESTful way.
from scraper import ShopifyScraper
from models import BrandContext

app = FastAPI(title="Shopify Insights Fetcher")

@app.get("/fetch-insights", response_model=BrandContext)
def fetch_insights(website_url: str = Query(..., description="Shopify store URL")):
    try:
        scraper = ShopifyScraper(website_url)
        return scraper.get_brand_context()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=401, detail="Website not found or inaccessible")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

