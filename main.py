import sys
import asyncio
from crawl import crawl_site_async
from csv_report import write_csv_report


async def main_async():
    base_url = sys.argv[1]
    max_concurrency = int(sys.argv[2])
    max_pages = int(sys.argv[3])
    page_data = await crawl_site_async(base_url, max_concurrency, max_pages)

    write_csv_report(page_data)


if __name__ == "__main__":
    asyncio.run(main_async())
