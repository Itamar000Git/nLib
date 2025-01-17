from enum import Enum

import pandas as pd


class Genre(Enum):
    FICTION = "Fiction"
    DYSTOPIAN = "Dystopian"
    CLASSIC = "Classic"
    ADVENTURE = "Adventure"
    ROMANCE = "Romance"
    HISTORICAL_FICTION = "Historical Fiction"
    PSYCHOLOGICAL_DRAMA = "Psychological Drama"
    PHILOSOPHY = "Philosophy"
    EPIC_POETRY = "Epic Poetry"
    GOTHIC_FICTION = "Gothic Fiction"
    GOTHIC_ROMANCE = "Gothic Romance"
    REALISM = "Realism"
    MODERNISM = "Modernism"
    SATIRE = "Satire"
    SCIENCE_FICTION = "Science Fiction"
    FANTASY = "Fantasy"
    TRAGEDY = "Tragedy"

class Book:
    def __init__(self, title, author, is_loaned, copies, genre, year):
        self.__title = title
        self.__author = author
        self.__is_loaned = is_loaned
        self.__copies = copies
        self.__genre = genre
        self.__year = year

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_is_loaned(self):
        return self.__is_loaned

    def get_copies(self):
        return self.__copies

    def get_genre(self):
        return self.__genre

    def get_year(self):
        return self.__year

    def get_loan_counter(self):
        return self.__loan_counter

    def set_loan_counter(self, loan_counter):
        self.__loan_counter = loan_counter

    # __str__ for human-readable string representation
    def __str__(self):
        return f'{self.get_title()}, {self.get_author()}, {self.get_is_loaned()}, {self.get_copies()}, {self.get_genre()}, {self.get_year()}'

    # __repr__ for unambiguous representation of the object
    def __repr__(self):
        return f'{self.get_title()}, {self.get_author()}, {self.get_is_loaned()}, {self.get_copies()}, {self.get_genre()}, {self.get_year()}'

    # Factory Method
    @staticmethod
    def create_book(title, author, is_loaned, copies, genre, year):
        try:
            genre_enum = Genre[genre.upper().replace(" ", "_")]  # Convert string to enum value
            return Book(title, author, is_loaned, copies, genre_enum, year)
        except KeyError:
            raise ValueError("Unknown genre")
