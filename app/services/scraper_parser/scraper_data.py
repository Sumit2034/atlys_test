from app.models.product import ProductDocument
from app.services.notification.notifier import Notifier
from app.services.scraper.scraper import Scraper


class ScraperData:

    """this class will process the scraped data"""
    
    def __init__(self, settings):
        self.settings = settings

    async def process(self):
        scraper = Scraper(scraper_params=self.settings)
        products = await scraper.scrape()
        
        from app.main import product_cache # this is done due to circular import
        for product in products:
            cached_value =  await product_cache.get_product_cache(key=product.name)
            breakpoint()
            if cached_value and cached_value['price'] != product.price:
                doc = await ProductDocument.get_by_name(name=product.name)
                doc.price = product.price
                await doc.replace()
            elif not cached_value:
                await ProductDocument.insert(product)
        
        # with open('products.json', 'w') as f:
        #     json.dump([product.dict() for product in products], f, indent=4)
        await Notifier.notify(f"Scraped {len(products)} products and updated the database.")
        print(f"Scraped {len(products)} products and updated the database.")
        return len(products)