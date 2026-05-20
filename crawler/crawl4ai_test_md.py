import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator



async def main():

    # configure the browser
    browser_conf = BrowserConfig(
        # or False to see the browser
        headless=True,
    )

    md_generator = DefaultMarkdownGenerator(
        content_source="clean_html",
    )

    run_conf = CrawlerRunConfig(
        # Set the cache mode to BYPASS to ensure that the crawler fetches fresh content from the web
        # CacheMode.ENABLED, CacheMode.DISABLED, CacheMode.BYPASS
        cache_mode=CacheMode.BYPASS,

        css_selector="div.main-area.article-area > article.article",
        excluded_selector=".code-block-extension-header",

        # add markdown generator
        markdown_generator=md_generator,
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url="https://article.juejin.cn/post/7455341128783839259",
            config=run_conf,
        )

        print(result.markdown.raw_markdown)
        # print(result.html)



if __name__ == "__main__":
    asyncio.run(main())
