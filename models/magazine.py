from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self._id = id
        self.name = name
        self.category = category
        if not self._id:
            self._create_magazine_in_db()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int):
            self._id = value
        else:
            raise ValueError("ID must be of type integer")
        
    @property
    def name(self):
        return self._name 

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if not 2 <= len(value) <= 16:
            raise ValueError("Name must be between 2 and 16 characters long")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise ValueError("Category must be a string")
        if len(value) == 0:
            raise ValueError("Category must be longer than 0 characters")
        self._category = value

    def _create_magazine_in_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self._name, self._category))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS magazines')
        conn.commit()
        conn.close()

    @classmethod
    def create_table(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        return magazine

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines')
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row[1], row[2], row[0]) for row in rows]

    @classmethod
    def get_by_id(cls, magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (magazine_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Magazine(row[1], row[2], row[0])
        return None

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE magazines SET name = ?, category = ? WHERE id = ?', (self.name, self.category, self.id))
        conn.commit()
        conn.close()

    def delete(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM magazines WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.title, a.content FROM articles a
            JOIN magazines m ON a.magazine_id = m.id
            WHERE m.id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles

    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT au.id, au.name FROM authors au
            JOIN articles a ON au.id = a.author_id
            WHERE a.magazine_id = ?
        ''', (self.id,))
        contributors = cursor.fetchall()
        conn.close()
        return [Author(row[1], row[0]) for row in contributors]

    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title FROM articles
            WHERE magazine_id = ?
        ''', (self.id,))
        titles = cursor.fetchall()
        conn.close()
        return [title[0] for title in titles] if titles else None

    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT au.id, au.name FROM authors au
            JOIN (
                SELECT author_id, COUNT(*) as article_count FROM articles
                WHERE magazine_id = ?
                GROUP BY author_id
                HAVING article_count > 2
            ) fa ON au.id = fa.author_id
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(row[1], row[0]) for row in authors]

    def __repr__(self):
        return f'<Magazine {self.name}>'
