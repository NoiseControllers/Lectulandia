class BookModel(object):
    def __init__(self):
        self._id = None
        self._book_post = None
        self._links = []
        self._link_pdf = None
        self._link_epub = None

    def id(self):
        return self._id

    def set_id(self, new_value):
        self._id = new_value

    def book_post(self):
        return self._book_post

    def set_book_post(self, new_value):
        self._book_post = new_value

    def links(self):
        return self._links

    def set_links(self, new_value):
        self._links = new_value

    def link_pdf(self):
        return self._link_pdf

    def set_link_pdf(self, new_value):
        self._link_pdf = new_value

    def link_epub(self):
        return self._link_epub

    def set_link_epub(self, new_value):
        self._link_epub = new_value
