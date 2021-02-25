import csv
import os
import threading

from src.Domain.Models.Book.BookModel import BookModel

lock = threading.Lock()


def write_to_file(book: BookModel) -> None:
    lock.acquire()
    with open(f'{os.getcwd()}\\books.csv', 'a', newline='', encoding='utf-8') as file:
        header = ['id', 'wp_id', 'link_epub', 'link_pdf', 'links']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writerow(
            {
                'id': book.book_post(),
                'wp_id': book.id(),
                'link_epub': book.link_epub(),
                'link_pdf': book.link_pdf(),
                'links': book.links()
            }
        )

    lock.release()


def load_books() -> list:
    books = []
    try:
        with open(f'{os.getcwd()}\\books.csv') as csv_file:
            csv_reader = csv.reader(csv_file)

            for row in csv_reader:
                books.append(row[0])
    except FileNotFoundError:
        pass

    return books
