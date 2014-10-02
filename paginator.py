import requests
import bs4
import urlparse

class Scraper():
    """ Simple scraper with get_next_page method """

    def __init__(self):
        self.listings = 0


    def get_listings(self, url):
        resp = requests.get(url)
        soup = bs4.BeautifulSoup(resp.content)

        listings = soup.find_all('div', class_='jobCard')

        for listing in listings:
            self.listings += 1
            title = listing.find('a', class_='title').get_text()
            desc = listing.find('div', class_='desc').get_text()
        
            print self.listings, '-',  title

        baseurl =  urlparse.urlparse(url)[1]
        next_url = urlparse.urljoin( 'http://' + baseurl, self._get_next_page(soup))

        self.get_listings(next_url)


    def _get_next_page(self, soup):
        try:
            return soup.find('a', id='paginationNext').get('href')
        except AttributeError as e:
            print 'No more listings'
            raise SystemExit


if __name__ == '__main__':
    
    paginator = Scraper()
    paginator.get_listings(args.url)
