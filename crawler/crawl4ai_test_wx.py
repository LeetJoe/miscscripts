#!/usr/bin/env python3
import asyncio
import re

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

WECHAT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/148.0.0.0 Safari/537.36"
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/148.0.0.0 Safari/537.36"
)


def _clean_markdown(md: str) -> str:
    """Clean raw markdown: remove data-URI placeholder images and excessive blank lines.

    WeChat articles contain 1x1 SVG placeholder images as data URIs. These appear
    in two forms in the raw markdown:
    1. Complete:  ![alt](data:image/svg+xml,...)
    2. Broken across lines — the regex doesn't capture the closing ), leaving
       orphan lines like:  '%20fill='%23FFFFFF'...%3C/svg%3E)
    """
    # Remove complete markdown images with data: URIs
    md = re.sub(r'!\[[^\]]*\]\(data:[^\)]+\)', '', md)
    # Remove orphan URL-encoded SVG tail lines (from broken data-URI images)
    md = re.sub(r"^['\"]?%[0-9A-Fa-f]{2}.*%3C/svg%3E\)?['\"]?\s*$", '', md, flags=re.MULTILINE)
    # Remove lines that are just leftover encoded SVG fragments
    md = re.sub(r"^.*%3Csvg%20.*%3C/svg%3E.*$", '', md, flags=re.MULTILINE)
    # Remove javascript:void links
    md = re.sub(r'\[([^\]]*)\]\(javascript:void\\\(0\\\);\)', r'\1', md)
    # Collapse 3+ consecutive blank lines into 2
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip()


async def crawl_wechat_article(url: str) -> dict:
    browser_config = BrowserConfig(
        user_agent=WECHAT_USER_AGENT,
        headers={
            "Referer": "https://mp.weixin.qq.com/",
            "Accept-Language": "zh-CN,zh;q=0.9",
        },
    )

    # WeChat uses data-src for lazy-loaded images. This JS copies data-src -> src
    # so that the markdown generator can pick up the real image URLs.
    js_fix_lazy_images = """
    document.querySelectorAll('img[data-src]').forEach(img => {
        if (!img.src || img.src.startsWith('data:')) {
            img.src = img.getAttribute('data-src');
        }
    });
    """

    config = CrawlerRunConfig(
        css_selector="div.rich_media_area_primary_inner > #img-content",
        excluded_selector="div#js_novel_card",

        wait_for="css:#js_content",
        js_code=js_fix_lazy_images,

        markdown_generator=DefaultMarkdownGenerator(
            content_source="clean_html",
            options={"ignore_links": False},
        ),
        # word_count_threshold=10,
        # remove_overlay_elements=True,

    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url, config=config)

    raw_md = _clean_markdown(result.markdown.raw_markdown) if result.markdown else ""

    return {
        "raw_markdown": result.markdown.raw_markdown,
        "markdown":     raw_md,
    }


def main():
    url = "https://mp.weixin.qq.com/s/MBYYcVRt1J1lAXQ32wadSA"

    article = asyncio.run(crawl_wechat_article(url))

    print(article["markdown"])


if __name__ == "__main__":
    main()
