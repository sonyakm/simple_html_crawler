from crawler import main_crawl

def test_example():
    assert main_crawl('https://example.com') == ['https://example.com']
    