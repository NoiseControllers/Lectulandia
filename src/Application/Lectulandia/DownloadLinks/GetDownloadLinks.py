import time

from selenium.common.exceptions import JavascriptException

from src.Application.ServerResponse.ServerResponse import ServerResponse
from src.Infraestructure.Utils.BrowserDriver.BrowserDriver import BrowserDriver


class GetDownloadLinks:
    def __init__(self):
        self._server_response = ServerResponse()
        self._browser = BrowserDriver().init()
        self._base_url = 'https://www.lectulandia.co'

    def download_links(self, url: str) -> list:
        print(url)
        dom = self._server_response.send_requests(url)

        if dom is not None:
            title_book = dom.find('div', id='title').get_text()
            links_parent = dom.find('div', id='downloadContainer')
            links_parent = links_parent.find_all('a')

            links = []

            for link in links_parent:
                url = self._base_url + link['href']
                beeupload_link = self.__get_direct_link(url)
                links.append(beeupload_link)

            return links

    def __get_direct_link(self, link_pre_download: str):
        self._browser.get(link_pre_download)
        time.sleep(4)
        try:
            beeupload_link = self._browser.execute_script('return linkCode;')
            beeupload_link = 'http://www.beeupload.net/file/' + beeupload_link
        except JavascriptException:
            beeupload_link = None

        return beeupload_link
