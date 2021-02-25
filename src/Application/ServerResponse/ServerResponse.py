import requests
from bs4 import BeautifulSoup
import time


class ServerResponse:
    def __init__(self):
        self._user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

    def send_requests(self, url: str) -> BeautifulSoup:
        time.sleep(3)
        response = requests.get(url, headers={'user-Agent': self._user_agent})
        print(f'RESPONSE: {response.status_code}')

        if response.status_code == 503:
            print(f'[-] El servidor devolvio un codigo distinto al 200: recibido -> {response.status_code} volviendo a intentar en 5 segundos.')
            time.sleep(5)
            self.send_requests(url=url)

        if response.status_code == 200:
            return BeautifulSoup(response.content, 'lxml')
