from queue import Queue
import pyperclip
import re

from src.Domain.Repositories.BooksRepository import BookRepository
from src.Domain.Repositories.External.LectulandiaRepository import LectulandiaRepository
from src.Infraestructure.Utils.Files.ConfiManagement.ConfigManagement import ConfigManagement
from src.Infraestructure.Workers.DownloadWorker import DownloadWorker

config = ConfigManagement().config('DEFAULT')
queue = Queue()

books_repository = BookRepository()
respository = LectulandiaRepository(queue, books_repository)

PATTERN = r'lectulandia.*$'

for c in range(int(config['MAX_THREADS'])):
    download_worker = DownloadWorker(queue)
    download_worker.daemon = True
    download_worker.start()


def show_menu():
    print('1 ) Busqueda automatica.')
    print('2 ) Busqueda Manual (url).')
    print('3 ) Salir')
    option = input('Opción: ')

    if int(option) == 1:
        automatic_search()
    elif int(option) == 2:
        manual_search()
    elif int(option) == 3:
        exit(0)
    else:
        print('Opción Desconocida.')
        show_menu()


def automatic_search():
    print('[*] Iniciando modo automático.')

    respository.get_all_catalogue()

    queue.join()


def manual_search():
    print('[*] Copia el enlace de lectulandia y el sistema lo pegara automáticamente aquí.')
    link_lectulandia = get_link_valid()
    print(link_lectulandia)

    pattern = r'^.*(serie|autor|genero).*$'
    pattern_book = r'^.*(book).*$'

    if re.match(pattern, link_lectulandia):
        respository.get_all_catalogue_by_type(link_lectulandia)
        queue.join()
    elif re.match(pattern_book, link_lectulandia):
        respository.get_book(link_lectulandia)
        queue.join()
    else:
        print('[-] Link no valido. el link debe ser solo de /serie/*, /autor/*, /genero/* o /book/*')


def get_link_valid():
    while True:
        if re.search(PATTERN, pyperclip.paste()):
            return pyperclip.paste()


if __name__ == '__main__':
    try:
        show_menu()
    except KeyboardInterrupt:
        print('[*] Programa detenido por el usuario.')
        print('[*] Por favor espere, mientras se guardan los cambios.')
