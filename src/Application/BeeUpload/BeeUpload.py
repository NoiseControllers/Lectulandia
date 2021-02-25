import requests
from bs4 import BeautifulSoup


class BeeUpload:
    def __init__(self):
        self._base_url = 'http://www.beeupload.net'

    def get_link_direct_download(self, response: requests):
        dom = BeautifulSoup(response.content, 'lxml')

        href = dom.find('a', id='downloadB')['href']

        full_url = self._base_url + href
        return full_url
