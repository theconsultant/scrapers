import requests
import bs4

visited_urls = []
stored_urls = []

def get_links(url):
    """ Extract link urls from a tags """

    visited_urls.append(url)
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.content)
    links = [tag.get('href') for tag in soup.find_all('a')]

    for link in links:
        stored_urls.append(link)

    return links

def recurse(url):
    """ Recursivly extract links from a site """

    print "Beginning at %s" % url
    for i in get_links(url):
        print 'Found %s' % i
    
    print 'Beginning recurse of stored_urls'    
    for j in stored_urls:
        if j in visited_urls:
            print '%s BEEN THERE DONE THAT' % j
            continue
        print j
        get_links(j)


def nested():
    for i in get_links('http://devbox'):
        print '%s' % i
        for j in get_links(i):
            print '%s' % j
            for k in get_links(j):
                print '%s' % k
def main():
    print 'Found links:'
    for i in get_links('http://devbox'):
        print '%s' % i
        for m in get_links(i):
            print '%s' % m

    print 'Visited URLS:'
    for j in visited_urls:
        print j

    print 'Stored URLS:'
    for k in stored_urls:
        print k


recurse('http://devbox')
