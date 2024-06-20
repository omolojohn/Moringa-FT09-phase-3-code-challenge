from database.connection import get_db_connection
from database.setup import create_tables

class Article:
    def __init__(self, title, content, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create_table(cls):
        create_tables()

    @classmethod
    def drop_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS articles')
        conn.commit()
        conn.close()

    def save(self):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',  
                (self.title, self.content, self.author_id, self.magazine_id)  
            )
            self.id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def create(cls, title, content, author, magazine):
        article = cls(title, content, author.id, magazine.id)
        article.save()
        return article

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise ValueError("ID must be an integer")
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise ValueError("Title must be a string")
        if len(value) == 0:
            raise ValueError("Title must be longer than 0 characters")
        self._title = value

    def fetch_from_db(self, article_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM articles WHERE id = ?', (article_id,))
            article_data = cursor.fetchone()
            if article_data:
                self.id, self._title, self.content, self.author_id, self.magazine_id = article_data
            else:
                raise ValueError("Article with given ID does not exist in the database")
        finally:
            conn.close()

    def __repr__(self):
        return f'<Article {self.title}>'
