import requests
import bs4
import re
import urlparse
import argparse
import signal
import os

class Spider():

    def __init__(self):
        self.visited_urls = []
        self.stored_urls = []


    def _stop_crawling(self, signal, frame):
        """ SIGINT handler to save results and abort the program """
        self._save_results()
        del self.stored_urls


    def _get_subdomains(self):
        """ Parse visited_urls and retrieve subdomains """
        self.subdomains = set()

        for visited_url in self.visited_urls:
            fqdn = urlparse.urlparse(visited_url)[1]
            if self.domain_name in fqdn:
                if len(fqdn.split('.')) > 2:
                    self.subdomains.add(fqdn.split('.')[0])


    def _get_directories(self):
        """ Parse visited_urls and create a directory structure """
        pass

     
    def _save_results(self):
        """ Clean lists and write stored/visited/subdomains to disk """
        # Creates self.subdomains
        self._get_subdomains()

        # Remove dups, become sets
        self.stored_urls = set(self.stored_urls)
        self.visited_urls = set(self.visited_urls)

        # Sort, saved back to lists
        self.stored_urls = sorted(self.stored_urls)
        self.visited_urls = sorted(self.visited_urls)
        self.subdomains = sorted(self.subdomains)

        print 'Stored URLS: %i' % len(self.stored_urls)
        print 'Visited URLS: %i' % len(self.visited_urls)
        print 'Subdomains: %i' % len(self.subdomains)

        # ToDo Create a resutls dir for each site crawled
        filename_visited = self.domain_name + '/visited-urls' 
        filename_stored = self.domain_name + '/stored-urls' 
        filename_subdomain = self.domain_name + '/subdomains' 

        if not os.path.exists(self.domain_name):
            os.mkdir(self.domain_name)

        with open(filename_visited, 'w') as f_visited:
            for visited in self.visited_urls:
                if visited:
                    f_visited.write(visited + '\n')

        with open(filename_stored, 'w') as f_stored:
            for stored in self.stored_urls:
                if stored:
                    f_stored.write(stored + '\n')

        with open(filename_subdomain, 'w') as f_subdomain:
            for subdomain in self.subdomains:
                if subdomain:
                    f_subdomain.write(subdomain + '\n')

        """
        in popTag
            return self.currentTag
              File "spider.py", line 18, in _stop_crawling
                  self._save_results()
                    File "spider.py", line 72, in _save_results
                        f_stored.write(stored + '\n')
                        UnicodeEncodeError: 'ascii' codec can't encode character u'\xe7' in position 49: ordinal not in range(128)
        """

    def get_links(self, url):
        """ Extract link urls from <a> tags """
        # Register interrupt handler
        signal.signal(signal.SIGINT, self._stop_crawling)

        self.visited_urls.append(url)

        try:
            resp = requests.get(url)
        except:
            return None

        soup = bs4.BeautifulSoup(resp.content)
        links = [tag.get('href').strip() for tag in soup.find_all('a') if tag.get('href')]

        # ToDo Fixup relative links to absolute

        # Catch AttributeError and exit when _stop_crawling() is called
        try:
            for link in links:
                if not 'mailto:' in link[:7]:
                    self.stored_urls.append(link)
            return links
        except AttributeError as e:
            print '[*] Spider Aborted'
            raise SystemExit


    def crawl(self, url):
        """ Recursivly extract links starting with supplied url  """
        # Register interrupt handler
        signal.signal(signal.SIGINT, self._stop_crawling)
        
        # Test if URL has valid syntax
        if not 'http://' in url[:7]:
            if not 'https://' in url[:8]: 
                raise ValueError('%s is not a valid URL' % url)

        # Parse URL
        self.domain_name = urlparse.urlparse(url)[1]

        # Call get_links() to seed stored_urls with initial url
        print "[*] Starting at %s" % url
        for link in self.get_links(url):
            print 'Found %s' % link
        
        print '[*] Beginning crawling of stored URLs'
        for stored_url in self.stored_urls:
            if not re.search(self.domain_name, urlparse.urlparse(stored_url)[1]):
                continue
            if '%20%20%20' in stored_url:
                continue
            if stored_url in self.visited_urls:
                continue
            print stored_url 
            self.get_links(stored_url) 
        self._save_results()


def parse_arguments():
    """ Get command line arguments """
    parser = argparse.ArgumentParser(description='Web Spider')
    parser.add_argument('-u', '--url', help='url to crawl',
    required=True)

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    mySpider = Spider()
    mySpider.crawl(args.url)
