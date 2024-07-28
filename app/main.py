from fastapi import APIRouter, Body, Depends, FastAPI, Response, status

from app.authorizations.authenticate import get_authenticated_user
from app.caches.product_cache import ProductCache
from app.models.database import init_db
from app.request_validations.scraper_params import ScraperParams
from app.services.notification.notifier import Notifier
from app.services.scraper_parser.scraper_data import ScraperData

authenticated = APIRouter(dependencies=[Depends(get_authenticated_user)])

notifier = Notifier()

product_cache = ProductCache()
async def lifespan(app: FastAPI):
    await init_db()
    await product_cache.initialize()
    yield
    await product_cache.redis_client.close()

app = FastAPI(title="/atlys", lifespan=lifespan)
app.include_router(authenticated)


@app.post("/scrape", status_code=status.HTTP_200_OK)
async def scrape_data(response: Response, settings: ScraperParams = Body(...), token: str = Depends(get_authenticated_user), ):
    response_length = await ScraperData(settings=settings).process()
    return {
        "message": f"Successfully Scraped {response_length} products .",
        "pages_parsed":response_length,
        "error": [],
        "status_code": response.status_code
    }
