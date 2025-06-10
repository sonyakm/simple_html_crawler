Simple HTML Web Crawler

Simple code to scrape links from a HTML web site.

Examples:
```
from crawler import main_crawl

url = 'https://example.com'
list_of_links = main_crawl(url)
```

When called from the command line, the code defaults to writing the resulting list of links to a file called 'links.txt' 
``` > python crawler.py url_to_scrape [output_text_file_name] ```

Caveats:
- Does not work on non-HTML encoded website
- Does not use concurrency; will be slow on a site with many links to visit