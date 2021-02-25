from src.Domain.Models.Book.BookModel import BookModel
from src.Infraestructure.Utils.Mysql.MysqlConnector import MysqlConnector


class BookRepository:
    def __init__(self):
        self._my_db = MysqlConnector().connect()

    def check_book_exists(self, slug_book_title: str):
        my_cursor = self._my_db.cursor()

        sql = "SELECT ID FROM wpeo_posts WHERE post_name = %s"
        adr = (slug_book_title,)
        my_cursor.execute(sql, adr)

        results = my_cursor.fetchall()
        if len(results) > 0:
            return results[0][0]
        else:
            return None

    def update_wpeo_postmeta(self, book: BookModel):
        my_cursor = self._my_db.cursor()
        if book.link_pdf() is not None:
            sql = "UPDATE wpeo_postmeta SET meta_value= %s WHERE post_id = %s AND meta_key = 'televisor'"
            val = (book.link_pdf(), book.id())
            my_cursor.execute(sql, val)

        if book.link_epub() is not None:
            sql = "UPDATE wpeo_postmeta SET meta_value= %s WHERE post_id = %s AND meta_key = 'aforo'"
            val = (book.link_epub(), book.id())
            my_cursor.execute(sql, val)

        self._my_db.commit()

        if my_cursor.rowcount == 0:
            print('[-] Error a subir a BD')
