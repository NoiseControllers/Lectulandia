import time
from queue import Queue
from bs4 import BeautifulSoup
import re


from src.Application.Lectulandia.DownloadLinks.GetDownloadLinks import GetDownloadLinks
from src.Application.ServerResponse.ServerResponse import ServerResponse
from src.Domain.Models.Book.BookModel import BookModel
from src.Domain.Repositories.BooksRepository import BookRepository
from src.Infraestructure.Utils.FileManagement.csv.CsvManagement import load_books
from src.Infraestructure.Utils.Files.ConfiManagement.ConfigManagement import ConfigManagement


class LectulandiaRepository:
    def __init__(self, queue: Queue, book_repository: BookRepository):
        self._queue = queue
        self._book_repository = book_repository
        self._server_response = ServerResponse()
        self._download_links = GetDownloadLinks()
        self._books = load_books()
        self._base_url = 'https://www.lectulandia.cc'
        self._last_page = 0
        self._config = ConfigManagement().config('DEFAULT')

    def get_all_catalogue(self):
        for page in range(int(self._config['START_PAGE']), int(self._config['LAST_PAGE']) + 1):
            url = self._base_url + f'/book/page/{str(page)}/'
            dom = self._server_response.send_requests(url)

            print(f'[*] Pagina: {str(page)} de {str(self._config["LAST_PAGE"])}')

            articles = dom.find_all('article', class_='card')

            for article in articles:
                article_id = article['id']

                if article_id in self._books:
                    continue

                href = article.find('a')['href']

                print(href)
                time.sleep(0.5)
                book_id = self._book_repository.check_book_exists(self.__clean_href(href))

                if book_id is None:
                    continue

                book = self.book_init_model(book_id, article_id, href)

                self._queue.put(book)

                del book
        print('[*] Todos los libros ya estan añadidos en cola.')

    def get_all_catalogue_by_type(self, url: str, page=1):
        print(f'URL: {url} PAGE: {page}')
        full_url = f'{url}page/{page}'
        dom = self._server_response.send_requests(full_url)

        if dom is None:
            print('NONE DETECTADO')

        articles = dom.find_all('article', class_='card')

        for article in articles:
            article_id = article['id']

            if article_id in self._books:
                continue

            href = article.find('a')['href']

            print(href)
            time.sleep(0.5)
            book_id = self._book_repository.check_book_exists(self.__clean_href(href))

            if book_id is None:
                continue

            book = self.book_init_model(book_id, article_id, href)
            self._queue.put(book)
            del book

        next_page = dom.find('a', text='Siguiente ››')

        if next_page is not None:
            page = page + 1
            self.get_all_catalogue_by_type(url=url, page=page)

    def book_init_model(self, book_id: int, article_id: str, href: str) -> BookModel:
        book = BookModel()

        book.set_id(book_id)
        book.set_book_post(article_id)

        if re.search(r'lectulandia', href):
            full_url = href
        else:
            full_url = self._base_url + href

        links = self._download_links.download_links(full_url)
        book.set_links(links)

        return book

    def get_book(self, href: str):
        book_id = self._book_repository.check_book_exists(self.__slug_href(href))
        if book_id is not None:
            dom = self._server_response.send_requests(href)
            article_id = dom.find('input', id='report')['data']
            article_id = f'post-{article_id}'
            book = self.book_init_model(book_id, article_id, href)
            self._queue.put(book)

    @staticmethod
    def __get_last_page(dom: BeautifulSoup) -> int:
        x = dom.find('div', class_='page-nav')
        total_pages = x.find_all_next('a')[2].get_text()
        total_pages = total_pages.replace('.', '')
        return int(total_pages)

    @staticmethod
    def __clean_href(link: str):
        link = link.replace('/book/', '')
        link = link.replace('/', '')
        return link

    @staticmethod
    def __slug_href(link: str):
        link = link.split('/')

        return link[4]
