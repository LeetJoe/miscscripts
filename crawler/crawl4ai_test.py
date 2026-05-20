import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator



async def main():

    # or False to see the browser
    browser_conf = BrowserConfig(headless=True)

    # markdown generator with a content filter that prunes content with a score below 0.4
    md_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed")
    )

    run_conf = CrawlerRunConfig(
        # Set the cache mode to BYPASS to ensure that the crawler fetches fresh content from the web
        # CacheMode.ENABLED, CacheMode.DISABLED, CacheMode.BYPASS
        cache_mode=CacheMode.BYPASS,

        # add markdown generator
        markdown_generator=md_generator,
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url="https://article.juejin.cn/post/7455341128783839259",
            config=run_conf,
        )


        print(result.markdown.raw_markdown)

        print('------------------\n')

        print(result.markdown.fit_markdown)



if __name__ == "__main__":
    asyncio.run(main())
