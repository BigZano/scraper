from urllib.parse import urlparse, urljoin
import asyncio
from bs4 import BeautifulSoup
import aiohttp


def normalize_url(url):
    parsed_url = urlparse(url)
    full_path = f"{parsed_url.netloc}{parsed_url.path}"
    full_path = full_path.rstrip("/")
    return full_path.lower()


from extract_url import get_urls_from_html
from extract_image import get_images_from_html
from text_parsing import get_h1_from_html, get_first_paragraph_from_html


def extract_page_data(html, page_url):
    return {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }


# AsyncCrawler implementation follows
class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}  # Stores fully crawled page data
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()  # Stores all active asyncio tasks
        self.semaphore = asyncio.Semaphore(self.max_concurrency)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={"User-Agent": "BootCrawler/1.0"})
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    # The crucial add_page_visit logic
    async def add_page_visit(self, normalized_url):
        async with self.lock:
            # 1. Check if the crawler has already received a stop signal
            if self.should_stop:
                return False

            # 2. Check if this specific URL has already been fully processed
            if normalized_url in self.page_data:
                return False  # It's a duplicate, don't process again

            # 3. Check if we have already reached the maximum number of *fully processed* pages.
            # This check happens here, before allowing a new page to be processed.
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True  # Set the stop flag
                print("Reached maximum number of pages to crawl.")
                # Cancel all running tasks
                for task in list(
                    self.all_tasks
                ):  # Use list() to avoid issues if set changes during iteration
                    if not task.done():  # Only try to cancel if it's not already done
                        task.cancel()
                return False  # Do not process this new page, we're at the limit

            # If we reached here, it's a new URL and we haven't hit the max_pages limit yet.
            # It will be added to self.page_data *after* successful processing in crawl_page.
            return True

    async def get_html(self, url):
        try:
            async with self.session.get(url) as response:
                if response.status > 399:  # Changed from >= 400 to > 399 for exactness
                    print(f"Error: HTTP {response.status} for {url}")
                    return None

                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    print(f"Error: Non-HTML content {content_type} for {url}")
                    return None

                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    async def crawl_page(self, current_url):
        # Always check should_stop first
        if self.should_stop:
            return

        current_url_obj = urlparse(current_url)
        if current_url_obj.netloc != self.base_domain:
            return  # Skip URLs outside the base domain

        normalized_url = normalize_url(current_url)

        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return  # Either already crawled, or max_pages was hit, or stop signal received

        async with self.semaphore:
            print(f"crawling {current_url}")
            html = await self.get_html(current_url)
            if html is None:
                # If HTML couldn't be fetched, we just return.
                # add_page_visit no longer adds a placeholder, so no need to delete.
                return

            page_info = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_url] = page_info  # Add fully processed data

            next_urls = get_urls_from_html(html, self.base_url)

        # Check should_stop *again* after fetching/processing and before creating new tasks
        if self.should_stop:
            return

        tasks = []
        for next_url in next_urls:
            task = asyncio.create_task(self.crawl_page(next_url))
            tasks.append(task)
            self.all_tasks.add(task)

        if tasks:
            try:
                # Use return_exceptions=True to allow CancelledError to be passed through
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                # Remove tasks from all_tasks set once they complete or are cancelled
                for task in tasks:
                    self.all_tasks.discard(task)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data


# The main entry point function
async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        # Initial call to crawl from the base_url
        await crawler.crawl()
        # Return the page_data *after* the crawl is complete
        return crawler.page_data
