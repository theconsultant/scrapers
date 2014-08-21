import requests
import bs4

r = requests.get('http://pcsupport.about.com/od/tipstricks/a/free-public-dns-servers.htm')
soup = bs4.BeautifulSoup(r.content)

def get_data(row):
    """Extract table data from rows -> data dict()"""
    data = {}
    tds = row.find_all('td')
    if tds:
        data= {'provider': tds[0].find('a').get_text().strip(),
               'primary': tds[1].get_text().strip(),
               'secondary': tds[2].get_text().strip()
        }
    return data


def print_results(dns_data):
    """Print dns data to stdout"""
    if len(dns_data['provider']) <= 7:
        print "%s\t\t\t%s\t%s" % (dns_data['provider'], dns_data['primary'], dns_data['secondary'])
    elif len(dns_data['provider']) <= 15:
        print "%s\t\t%s\t%s" % (dns_data['provider'], dns_data['primary'], dns_data['secondary'])
    else:
        print "%s\t%s\t%s" % (dns_data['provider'], dns_data['primary'], dns_data['secondary'])


if __name__ == '__main__':
    table = soup.find('table')
    rows = table.find_all('tr')

    for row in rows:
        dns_data = get_data(row)
        if dns_data:
            print_results(dns_data)
