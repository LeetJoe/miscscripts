### 学习笔记

从实用角度来看，主要有两种 crawl 结果，一种是基于 filter 的 markdown 抓取，一种是基于 schema 的 json 抓取。

#### 通用：html 处理

1. 首先 crawler 按 `CrawlerRunConfig` 中的 `css_selector` 或 `target_elements` 里的选择器选择整个页面中的内容，得到 `raw_html`；
2. 如果 `CrawlerRunConfig` 中配置了 `excluded_selector`, `excluded_tags` 等，会基于这些规则对 `raw_html` 进行处理，得到 `clean_html`；

在这个步骤中，通过 `css_selector` 获取主体内容 `raw_html`，再使用规则过滤得到 `clean_html`。

#### markdown 抓取

1. 如果 `DefaultMarkdownGenerator` 配置了 `content_filter`，则默认使用 `clean_html`，应用 filter 之后得到 `fit_html`，在此基础上生成 markdown.raw_markdown 和 markdown.fit_markdown；
2. 如果没有配置 `content_filter`，则默认使用 `clean_html` 来生成 markdown.raw_markdown, fit_markdown 为空；
3. 在没有配置 `content_filter` 的情况下，通过指定 `content_source` 是 `raw_html`, `clean_html`, 还是 `fit_html` 来生成 markdown.raw_markdown 结果；
4. 在使用任何 `content_filter` 之前，`fit_html` 是空的，所以 markdown.fit_markdown 也是空的；
5. 在生成的 `CrawlerResult` 对象 result 后，默认生成结果（基于`clean_html`）放在 `result.markdown.raw_markdown` 里；如果生成的时候配置了 filter，则会再生成一份 `fit_markdown`，里面是应用了 filter 的生成结果，即 markdown.fit_markdown；

由于 filter 的以打分的方式或者 LLM 的方式进行过滤，工作方式不太明确，所以一般的处理流程是，显式指定 `content_source` 为 `clean_html`，不使用 filter，就能从 `clean_html` 里提取相应的 markdown 内容，通过 markdown.raw_markdown 获取；这个处理流能满足大多数文章抓取的需求。


#### json 抓取

1. 通过 c4a assistant 浏览器插件，生成 schema；
2. 基于 schema 配置 `JsonCssExtractionStrategy`；
3. 将 strategy 配置到 `CrawlerRunConfig` 的 `extraction_strategy` 属性里；
4. `result.extracted_content` 就是按 schema 提取的 json 串。

由于 schema 能精确地指定元素，这种方式适合精细地提供内容条目，适合页面中多条内容的获取；配置 field 的时候要尽可能细，在预览里能看到有效内容才行；如果配置的范围太大，可能取不到任何结果。
