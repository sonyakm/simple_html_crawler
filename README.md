Simple HTML Web Crawler

Simple code to scrape links from a HTML web site.

Examples:
```
from crawler import main_crawl

url = 'https://example.com'
list_of_links = main_crawl(url)
```

When called from the command line, the code defaults to writing the resulting list of links to a file called 'links.txt'.  Example command line call:
``` > python crawler.py books.toscrape.com book_links.txt ```

Two very simple tests included to test a simple site crawl output and one bad input

Caveats:
- Does not work on non-HTML encoded website
- Even with using concurrency, this code may be slow to run on large websites
- Would likely include sleeps/delays if it were to be used in production to avoid multiple rapid-fire hits on a website/domain
- Would likely include more "bad" tests if it were to be used in production

Last Updated: skm/June 2025