import sys
from urllib2 import urlopen, URLError
from argparse import ArgumentParser
from bs4 import BeautifulSoup

# ToDo
# Use classes
# Make output useful for other programs


def parse_arguments():
    """ Process command line arguments """
    parser = ArgumentParser(description='Grabs tables from html')
    parser.add_argument('-u', '--url', help='url to grab from',
                        required=True)
    args = parser.parse_args()
    return args


def parse_rows(rows):
    """ Get data from rows """
    results = []
    for row in rows:
        table_data = row.find_all(['th', 'td'])
        if table_data:
            results.append([data.get_text().strip() for data in table_data])
    return results


def main():
    # Get arguments
    args = parse_arguments()
    url = args.url

    try:
        resp = urlopen(url)
    except URLError as e:
        raise ValueError('Error fetching - %s' %  e.reason)   
    soup = BeautifulSoup(resp.read())
    
    try:
        table = soup.find('table')
        rows = table.find_all('tr')
    except AttributeError as e:
        raise ValueError('No valid table found')

    table_data = parse_rows(rows)

    for i in table_data:
       print '\t'.join(i)


if __name__ == '__main__':
    main()
