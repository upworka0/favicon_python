from bs4 import BeautifulSoup
import requests

from urllib.parse import urlparse
import os


# initial variables
filepath = "urls.txt"


def getDomain(url):
    """
    Get domain uri from url
    :param url: string
    :return: string
    """
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

def getExtension(url):
    try:
        name, ext = os.path.splitext(url)
        return ext.replace('.','')
    except:
        return 'ico'

def Filename(url):
    if 'http' not in url:
        url = 'http://' + url
    """
    Generate file name from url
    :param url: string
    :return: string
    """
    parsed_uri = urlparse(url)
    return parsed_uri.netloc


def download(url, icoName):
    """
    Download fav icon from url
    :param url: string
    :param originurl:  string
    :return: None
    """
    response = requests.get(url, stream=True)

    if response.status_code < 300:
        with open('icons/{}.{}'.format(icoName, getExtension(url)), 'wb') as image:
            for chunk in response.iter_content(1024):
                image.write(chunk)
        print("downloaded icon %s" % icoName)
    else:
        print("There is not ico named %s " % icoName)

def getFaviconLink(domain):
    if 'http' not in domain:
        domain = 'http://' + domain
    page = requests.get(domain)

    soup = BeautifulSoup(page.text, features="lxml")
    icon_link = soup.find("link", rel="shortcut icon")
    if icon_link is None:
        icon_link = soup.find("link", rel="icon")

    if icon_link is None:
        return getDomain(domain) + '/favicon.ico'
    return icon_link["href"]


if __name__ == '__main__':
    # create icons folder if not existed
    if not os.path.exists('icons'):
        os.makedirs('icons')

    # read urls from domains.txt file
    file = open(filepath, 'r')
    urls = file.readlines()

    # download favico from url
    for url in urls:
        try:
            _row_dt = url.strip().split(';')
            url = _row_dt[0].strip()
            icoName = _row_dt[1]
            icoUrl = getFaviconLink(url)
            if not 'http' in icoUrl and '//' in icoUrl:
                icoUrl = 'http:' + icoUrl
            elif not 'http' in icoUrl:
                icoUrl = getDomain(url) + icoUrl
            download(icoUrl, icoName)
        except Exception as e:
            print(e)
            print("There is not ico in %s " % url)