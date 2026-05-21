import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, DefaultTableExtraction
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator



async def main():

    # configure the browser
    browser_conf = BrowserConfig(
        # or False to see the browser
        # headless=True,
    )

    md_generator = DefaultMarkdownGenerator(
        content_source="clean_html",
    )

    run_conf = CrawlerRunConfig(
        # Set the cache mode to BYPASS to ensure that the crawler fetches fresh content from the web
        # CacheMode.ENABLED, CacheMode.DISABLED, CacheMode.BYPASS
        cache_mode=CacheMode.BYPASS,

        css_selector="div.wrapper-content > div.detail-content",
        excluded_selector=".detail-title-des",

        # add markdown generator
        markdown_generator=md_generator,

        # table_extraction=DefaultTableExtraction(table_score_threshold=-3)
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url="https://www.stats.gov.cn/sj/zxfb/202605/t20260518_1963732.html",
            config=run_conf,
        )

        print(result.markdown.raw_markdown)
        # print(result.html)



if __name__ == "__main__":
    asyncio.run(main())
