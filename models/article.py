from database.connection import get_db_connection
from database.setup import create_tables
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, title, content, author, magazine, id=None):
        self._id = id
        self.title = title
        self.content = content
        self.author = author
        self.magazine = magazine
        if not self._id:
            self._create_article_in_db()

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

    def _create_article_in_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
            (self._title, self.content, self.author.id, self.magazine.id)
        )
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def create(cls, title, content, author, magazine):
        article = cls(title, content, author, magazine)
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
        if not 5 <= len(value) <= 50:
            raise ValueError("Title must be between 5 and 50 characters long")
        self._title = value

    def fetch_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author.id,))
        author_data = cursor.fetchone()
        conn.close()
        if author_data:
            return Author(author_data[1], author_data[0])
        else:
            raise ValueError("Author with given ID does not exist")

    def fetch_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine.id,))
        magazine_data = cursor.fetchone()
        conn.close()
        if magazine_data:
            return Magazine(magazine_data[1], magazine_data[2], magazine_data[0])
        else:
            raise ValueError("Magazine with given ID does not exist")

    def save(self):
        if not self._id:
            self._create_article_in_db()
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ? WHERE id = ?',
                (self.title, self.content, self.author.id, self.magazine.id, self._id)
            )
            conn.commit()
            conn.close()

    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM articles WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()

    def __repr__(self):
        return f'<Article {self.title}>'
