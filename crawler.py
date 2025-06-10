import sys
from urllib.parse import urlparse, urljoin
import urllib.robotparser
from bs4 import BeautifulSoup
import requests

USER_AGENT="MySimpleCrawler"

'''
    Simple HTML web crawler that visits links in the same subdomain
    URLs are printed in a text file
'''

def check_valid(url):
    '''
    Check if the URL is valid and remove any trailing fragments

    Arg: url 

    Returns: url (with scheme added) or None if url is invalid
    '''

    if not url:
        return None
    if not urlparse(url).scheme:
        url = "http://"+url
    try:
        parsed = urlparse(url)
        if not parsed.scheme and not parsed.netloc:
            return None # Not a proper URL

        if not '.' in parsed.netloc:
            return None # Not a proper domain

        # Remove fragments
        new_url = parsed._replace(fragment="").geturl()

    except:
        print(f"Error parsing URL '{url}'")
        return None

    try:
        headers = {'User-Agent': USER_AGENT }
        response = requests.get(new_url, timeout=10, headers=headers)
        response.raise_for_status()  # HTTPerror
    except:
        print(f"Not a valid URL {url}")
        return None

    return new_url

def get_robot_txt(url):
    '''
    Gets information from the robots.txt file on the website to be scraped.
    Script will use robots.txt to see if we are allowed to scrape the URL.

    Arg: url (already validated with check_valid)

    Returns: robot_parser object    
    '''
    parsed = urlparse(url)
    robot_url = urljoin(f"{parsed.scheme}://{parsed.netloc}",'robots.txt')
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robot_url)
        rp.read()
        return rp
    except:
        print('no robots.txt file; proceeding without limitations')
        return None

def get_links_from_url(url, robot=None):
    '''
    Checks link for validity.
    Makes sure we are allowed to fetch the site.
    Grabs links from the site.

    Args: url: URL for the site
          robot: robot parser with robots.txt info in it

    Returns:
        list of links
        None if errors
    '''

    url = check_valid(url)
    if not url:
        return None

    if robot:
        if not robot.can_fetch(USER_AGENT, url):
            return None

    try:
        headers = {'User-Agent': USER_AGENT }
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()  # HTTPerror
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    if 'text/html' not in response.headers.get('Content-Type', ''):
        return None #ignore non-HTML content

    soup = BeautifulSoup(response.text, 'html.parser')
    found_links = []
    for link_tag in soup.find_all('a', href=True):
        link_href = link_tag['href']
        abs_url = urljoin(url, link_href)
        found_links.append(abs_url)

    return found_links

def main_crawl(url):
    ''' 
    main control routine for crawler program
    Args:
        url : base URL to scrape

    Returns:
        list of links starting from url
            (None if there are errors)     
    '''

    #Check initial URL for validity
    url = check_valid(url)
    if not url:
        return None

    #Check robots.txt file
    rp = get_robot_txt(url)

    #Create visited URL list
    visited =[]

    #Create queue for URLs to visit
    url_queue = [url]

    #For checking that links are in the proper subdomain
    parsed_orig = urlparse(url)
    subdomain = f"{parsed_orig.netloc}/{parsed_orig.path}"

    while url_queue:
        myurl = url_queue.pop()

        if not check_valid(myurl):
            continue #skip if not url

        if myurl in visited:
            continue #skip if visited
        visited.append(myurl)

        mylinks = get_links_from_url (myurl,robot=rp) #get list of links

        if mylinks:
            for follow_url in mylinks:
                #Have we already visited it?
                if (follow_url in visited) or (follow_url.rstrip('/') in visited):
                    continue

                #Is it from the same base domain as the original URL?
                if subdomain in follow_url:
                    url_queue.append(follow_url) #append to end of queue

    return visited


if __name__ == "__main__":

    #If called from command line, can call with one or two arguments:
    #URL to scrape and output filename (optional)

    if len(sys.argv) > 1:
        testurl = sys.argv[1]
        if len(sys.argv) > 2:
            outfile = sys.argv[2]
        else:
            outfile = 'links.txt'
    else:
        print(f"USAGE: python {sys.argv[0]} url_to_scrape [output_text_file_name]")
        sys.exit(1)

    links = main_crawl(testurl)
    if links:
        with open(outfile,"w") as file:
            file.write(f"Crawler output for {testurl}:\n")
            _ = [file.write(f"{line}\n") for line in links]
