from database.connection import get_db_connection
from database.setup import create_tables

class Author:
    def __init__(self, name, id=None):
        self._id = id
        self.name = name
        if not self._id:
            self._create_author_in_db()

    @classmethod
    def create_table(cls):
        create_tables()

    @classmethod
    def drop_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS authors')
        conn.commit()
        conn.close()

    def _create_author_in_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def create(cls, name):
        author = cls(name)
        return author

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if hasattr(self, '_name'):
            raise AttributeError("Cannot change the author's name after it is set")
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) == 0:
            raise ValueError("Name must be longer than 0 characters")
        self._name = value

    def fetch_from_db(self, author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (author_id,))
        author_data = cursor.fetchone()
        conn.close()
        if author_data:
            self._id = author_data[0]
            self._name = author_data[1]
        else:
            raise ValueError("Author with given ID does not exist in the database")

    def save(self):
        if not self._id:
            self._create_author_in_db()
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE authors SET name = ? WHERE id = ?', (self._name, self._id))
            conn.commit()
            conn.close()

    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM authors WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.title, a.content FROM articles a
            JOIN authors au ON a.author_id = au.id
            WHERE au.id = ?
        ''', (self._id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT m.id, m.name, m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        ''', (self._id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines

    def __repr__(self):
        return f'<Author {self.name}>'
