import httpx
import bs4
from playwright.async_api import async_playwright
import asyncio
import re
from app.logger import setup_logger

logger = setup_logger(__name__)

class Scraper():

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        
    async def _init_playwright(self):
        """Initializes Playwright"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        )
        
    async def _cleanup_playwright(self):
        """Cleanup Playwright resources"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            
    def process(self, text):
        cleaned = re.sub(r"[^a-zA-Z0-9\s.,!?;:\'\"-]", "", text)
    # Clean up multiple spaces
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned.strip()

    async def scrape_with_bs4(self, url):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/139.0.0.0 Safari/537.36"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url, headers=headers)
            
                soup = bs4.BeautifulSoup(response.content, 'html.parser')
                
                for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
                    tag.decompose()

                content = soup.get_text(separator=" ", strip=True)
            
                return {
                    "url": url,
                    "title": soup.title.string if soup.title else '',
                    "text": content[:10000],
                    "method": "beautifulsoup",
                    "success": True,
                    "error": None
                }
                
        except Exception as e:
            logger.error(f"BS4 failed: {e}")
            return None

    async def scrape_with_playwright(self, url):

        try:
            
            page = await self.context.new_page()
            await page.goto(url, wait_until='networkidle', timeout=30000)
            await asyncio.sleep(2)
            
            text = await page.inner_text('body')
            text = self.process(text)
            
            title = await page.title()
            title = self.process(title)
            
            await page.close()
            
            return {
                "url": url,
                "title": title,
                "text": text[:10000],
                "method": "playwright",
                "success": True,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Playwright failed: {e}")
            return {
                'url': url,
                'title': '',       
                'text': '',        
                'error': str(e)[:500],  
                'method': 'playwright',
                'success': False
            }
    
    async def is_content_sufficient(self, result, min_length=500):
        
        if not result or not result.get('text'):
            return False
        
        text_length = len(result["text"])
        
        return text_length > min_length
    
    async def scrape_url(self, url):
        
        result = await self.scrape_with_bs4(url)
        
        if await self.is_content_sufficient(result=result):
            logger.info(f"BS4 worked! Content length: {len(result['text'])}")
            return result
        
        
        result = await self.scrape_with_playwright(url)
        
        if result.get('success'):
            logger.info(f"Playwright worked! Content length: {len(result.get('text', ''))}")
        else:
            logger.error(f"Playwright failed for: {url}")
            
        return result
        
    async def scrape_multiple(self, urls):
        
        await self._init_playwright()
        
        # results = []
        # stats = {'beautifulsoup': 0, 'playwright': 0, 'failed': 0}
        
        #   For Sequential Scraping
        
        # for url in urls:
        #     result = await self.scrape_url(url)
            
        #     if result.get('success'):
        #         results.append(result)
        #         stats[result["method"]] += 1
        #     else:
        #         stats['failed'] += 1
                
        #     await asyncio.sleep(1)
        
        # print(f"\n Stats: BS4={stats['beautifulsoup']}, "
        #       f"Playwright={stats['playwright']}, "
        #       f"Failed={stats['failed']}")
        
        # #   For parallel (Comment Above and Uncomment below)
        try:  
            results = await asyncio.gather(*[self.scrape_url(url) for url in urls]) #   "*" for unpacking {list is seen as single obj} .gather(list) => .gather(coroutine1, co2, co3 etc)
        
        finally:
            await self._cleanup_playwright()
        
        return results
        
async def search(query, categories):
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            # res = await client.get(f"http://search_engine:8080/search?q={query}&categories={categories}&format=json")
            res = await client.get("http://search_engine:8080/search", 
                                    params={
                                        "q": query,
                                        "categories": categories,
                                        "format": "json"
                                    })
            res.raise_for_status()
            return res.json()
    
    except Exception as e: 
        logger.error(f"Search failed: {e}")
        return {"results": []}
    
async def search_and_scrape(query, categories, data=None, maxURL=10):
    
    if not data: 
        data = await search(query, categories)
    urls = [page["url"] for page in data["results"] if page.get("url")][:maxURL]
    
    scraper = Scraper()
    results = await scraper.scrape_multiple(urls=urls)  
      
    return results
    
# if __name__ == "__main__":
    