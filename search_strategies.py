import pandas as pd
from abc import ABC, abstractmethod

available_df = pd.read_csv("available_books.csv")
loaned_df = pd.read_csv("loaned_books.csv")
# מיזוג הרשימות: כל הספרים ברשימה של הזמינים + ספרים ייחודיים מרשימת המושאלים
combined_books = pd.concat([available_df, loaned_df]).drop_duplicates(subset=['title', 'author'], keep='first')
# שמירת הרשימה המשולבת
combined_books.to_csv("combined_books.csv", index=False)
# הצגת הנתונים לדוגמה


# Strategy Interface
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, books_df, query):
        pass


# Search by Title
class SearchByTitle(SearchStrategy):
    def search(self, books_df, query):
        return books_df[books_df['title'].str.contains(query, case=False, na=False)]


# Search by Author
class SearchByAuthor(SearchStrategy):
    def search(self, books_df, query):
        return books_df[books_df['author'].str.contains(query, case=False, na=False)]


# Search by Year
class SearchByYear(SearchStrategy):
    def search(self, books_df, query):
        return books_df[books_df['year'] == int(query)]


# Search by Genre
class SearchByGenre(SearchStrategy):
    def search(self, books_df, query):
        return books_df[books_df['genre'].str.contains(query, case=False, na=False)]


# Context Class
class BookSearchContext:
    def __init__(self, strategy: SearchStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: SearchStrategy):
        self.strategy = strategy

    def search(self, books_df, query):
        return self.strategy.search(books_df, query)

def search_books(criterion, query):
    strategies = {
        "title": SearchByTitle(),
        "author": SearchByAuthor(),
        "year": SearchByYear(),
        "genre": SearchByGenre(),
    }

    if criterion not in strategies:
        print("Invalid search criterion! Choose from: title, author, year, genre, availability.")
        return None

    context = BookSearchContext(strategies[criterion])
    results = context.search(combined_books, query)
    return results
