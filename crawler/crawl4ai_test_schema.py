import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import JsonCssExtractionStrategy



async def main():

    # schema can generate from c4a assistant
    schema = {
        "name": "article.juejin.cn Schema",
        "baseSelector": "div.main-area.article-area > article.article",
        "fields": [
            {
            "name": "title",
            "selector": "h1.article-title",
            "type": "text"
            },
            {
            "name": "content",
            "selector": "#article-root > div.article-viewer.markdown-body",
            "type": "nested"
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
            url="https://article.juejin.cn/post/7455341128783839259",

            # crawler config
            config=run_conf,
        )


        data = json.loads(result.extracted_content)
        print(data)



if __name__ == "__main__":
    asyncio.run(main())
