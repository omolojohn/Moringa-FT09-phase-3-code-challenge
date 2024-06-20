from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

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
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters long")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string")

    def __repr__(self):
        return f'<Magazine {self.name}>'

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

    @staticmethod
    def create(name, category):
        if not name or not category:
            raise ValueError("Name and category are required")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (name, category))
        conn.commit()
        magazine_id = cursor.lastrowid
        conn.close()
        return Magazine(magazine_id, name, category)

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines')
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row[0], row[1], row[2]) for row in rows]

    @classmethod
    def get_by_id(cls, magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (magazine_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Magazine(row[0], row[1], row[2])
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
