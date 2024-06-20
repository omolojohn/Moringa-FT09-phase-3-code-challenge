import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author("John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        article = Article("Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_author_name_validation(self):
        with self.assertRaises(ValueError):
            Author("") 
        with self.assertRaises(ValueError):
            Author(123) 

    def test_author_save_and_fetch(self):
        Author.drop_table()
        Author.create_table()
        author = Author.create("John Doe")
        fetched_author = Author("placeholder")
        fetched_author.fetch_from_db(author.id)
        self.assertEqual(fetched_author.name, "John Doe")

    def test_article_title_validation(self):
        with self.assertRaises(ValueError):
            Article("", "Content", 1, 1)
        with self.assertRaises(ValueError):
            Article(123, "Content", 1, 1)  

    def test_magazine_name_validation(self):
        with self.assertRaises(ValueError):
            Magazine(1, "", "Category")
        with self.assertRaises(ValueError):
            Magazine(1, "A very long name that exceeds sixteen characters", "Category") 

    def test_magazine_category_validation(self):
        with self.assertRaises(ValueError):
            Magazine(1, "Valid Name", "") 

    def test_magazine_save_and_fetch(self):
        Magazine.drop_table()
        Magazine.create_table()
        magazine = Magazine.create("Tech Weekly", "Technology")
        fetched_magazine = Magazine.get_by_id(magazine.id)
        self.assertEqual(fetched_magazine.name, "Tech Weekly")
        self.assertEqual(fetched_magazine.category, "Technology")

    def test_author_delete(self):
        author = Author.create("John Doe")
        author_id = author.id
        author.delete()
        with self.assertRaises(ValueError):
            fetched_author = Author("placeholder")
            fetched_author.fetch_from_db(author_id) 

    def test_magazine_delete(self):
        magazine = Magazine.create("Tech Weekly", "Technology")
        magazine_id = magazine.id
        magazine.delete()
        self.assertIsNone(Magazine.get_by_id(magazine_id)) 

if __name__ == "__main__":
    unittest.main()
