import time
from queue import Queue
from threading import Thread
import requests
from src.Application.BeeUpload.BeeUpload import BeeUpload
import os

from src.Domain.Models.Book.BookModel import BookModel
from src.Domain.Repositories.BooksRepository import BookRepository
from src.Infraestructure.Utils.FileManagement.csv.CsvManagement import write_to_file
from src.Infraestructure.Utils.Files.UploadFiles.AnonFiles import AnonFiles


class DownloadWorker(Thread):
    def __init__(self, queue: Queue):
        self._queue = queue
        self._beeupload = BeeUpload()
        self._book = None  # type: BookModel
        self._anonfiles = AnonFiles()
        self._book_repository = BookRepository()
        super().__init__()

    def run(self) -> None:
        print('Iniciado?')
        while self._queue.all_tasks_done:
            self._book = self._queue.get()
            book = self._book  # type: BookModel

            file_name = None
            for link in book.links():
                if link is None:
                    continue

                print(f'[*] Download: {link}')

                file_name = self.__download(link)
                if file_name is None:
                    continue

                extension = file_name.split('.')[1]
                new_link_download = self._anonfiles.upload(file_name)

                if extension == 'pdf':
                    book.set_link_pdf(new_link_download)
                elif extension == 'epub':
                    book.set_link_epub(new_link_download)

            self._book_repository.update_wpeo_postmeta(book)
            write_to_file(book)
            self.__remove_file(file_name)
            del book

            self._queue.task_done()

    def __download(self, url: str):
        session = requests.Session()
        response = session.get(url)
        time.sleep(3)
        link_direct = self._beeupload.get_link_direct_download(response)
        print(link_direct)
        response = session.get(link_direct)

        if response.status_code == 200:
            content_type = response.headers['content-disposition']
            file_name_temp = self.__clean_filename(content_type)

            f = open(f'{os.getcwd()}\\temp\\{file_name_temp}', 'wb')
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
            f.close()

            return file_name_temp
        else:
            print(f'[-] No downloading {url} server not response')
        return None

    @staticmethod
    def __clean_filename(content_type: str):
        content_type = content_type.split('filename=')[1].replace('"', '').replace(' ', '-')
        return content_type

    @staticmethod
    def __remove_file(file_name: str):
        try:
            os.remove(f'{os.getcwd()}\\temp\\{file_name}')
        except (PermissionError, FileNotFoundError):
            pass
        except UnboundLocalError:
            pass

