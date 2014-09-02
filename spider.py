import requests
import bs4
import re
import urlparse
import argparse

class Spider():

    def __init__(self):
        self.visited_urls = []
        self.stored_urls = []

    def get_links(self, url):
        """ Extract link urls from <a> tags """

        # Test if URL has valid syntax
        if not 'http://' in url[:7] or 'https://' in url[:8]:
            return None
        
        self.visited_urls.append(url)
        try:
            resp = requests.get(url)
        except:
            return None

        soup = bs4.BeautifulSoup(resp.content)
        links = [tag.get('href') for tag in soup.find_all('a')]

        # ToDo Fixup relative links to absolute

        for link in links:
            if link:
                if not 'mailto:' in link[:7]:
                    self.stored_urls.append(link)
        return links

    def crawl(self, url):
        """ Recursivly extract links starting with supplied url  """
        
        # Test if URL has valid syntax
        if not 'http://' in url[:7] or 'https://' in url[:8]:
            raise ValueError('%s is not a valid URL' % url)

        # Parse URL
        url_parts = urlparse.urlparse(url)

        # Call get_links() to seed stored_urls with initial url
        print "Beginning at %s" % url
        for link in self.get_links(url):
            print 'Found %s' % link
        
        print 'Beginning crawling of stored_urls'    
        for stored_url in self.stored_urls:
            if not stored_url:
                continue
            if not re.search(url_parts.netloc, stored_url):
                continue
            if '%20%20%20' in stored_url:
                continue
            if stored_url in self.visited_urls:
                continue
            print stored_url 
            self.get_links(stored_url)

        # Remove dups, become sets
        self.stored_urls = set(self.stored_urls)
        self.visited_urls = set(self.visited_urls)

        # Sort, saved back to lists
        self.stored_urls = sorted(self.stored_urls)
        self.visited_urls = sorted(self.visited_urls)

        print 'Stored URLS: %i' % len(self.stored_urls)
        print 'Visited URLS: %i' % len(self.visited_urls)

        # ToDo Create a resutls dir for each site crawled
        filename_visited = 'visited-urls-' + url_parts.netloc
        filename_stored = 'stored-urls-' + url_parts.netloc

        with open(filename_visited, 'w') as f_visited:
            for visited in self.visited_urls:
                f_visited.write(visited + '\n')

        with open(filename_stored, 'w') as f_stored:
            for stored in self.stored_urls:
                if stored:
                    f_stored.write(stored + '\n')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Web Spider')
    parser.add_argument('-u', '--url', help='url to crawl',
    required=True)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    mySpider = Spider()
    mySpider.crawl(args.url)
