from models.article import Article
from models.magazine import Magazine
from models.author import Author

Author.drop_table()
Magazine.drop_table()
Article.drop_table()

Author.create_table()
Magazine.create_table()
Article.create_table()

author1=Author.create("George Otieno")
magazine1=Magazine.create("Sports Daily","Sports")
article1 = Article.create("Sports Daily News", "Trusted news", author1, magazine1)

print("Author id:",author1.id)
print("Author name",author1.name)