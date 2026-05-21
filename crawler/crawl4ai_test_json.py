import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import JsonCssExtractionStrategy



async def main():

    # schema can generate from c4a assistant
    schema = {
        "name": "News Items",
        "baseSelector": "tr.athing",
        "fields": [
            {"name": "title", "selector": "span.titleline a", "type": "text"},
            {
                "name": "link", 
                "selector": "span.titleline a", 
                "type": "attribute", 
                "attribute": "href"
            }
        ]
    }

    # schema based extraction strategy
    strategy = JsonCssExtractionStrategy(schema)


    # configure the browser
    browser_conf = BrowserConfig(
        # or False to see the browser
        headless=True,
    )

    run_conf = CrawlerRunConfig(
        # Set the cache mode to BYPASS to ensure that the crawler fetches fresh content from the web
        # CacheMode.ENABLED, CacheMode.DISABLED, CacheMode.BYPASS
        cache_mode=CacheMode.BYPASS,

        # add extraction strategy
        extraction_strategy=strategy
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url="https://news.ycombinator.com/newest",

            # crawler config
            config=run_conf,
        )


        data = json.loads(result.extracted_content)
        print(data)



if __name__ == "__main__":
    asyncio.run(main())
