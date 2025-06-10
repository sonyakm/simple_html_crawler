from crawler import main_crawl


def test_bad_input():
    assert main_crawl('badurl') == None

