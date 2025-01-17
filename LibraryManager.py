import csv
import os
from os.path import exists
import self
import GUI_Libarary
from Book import Book as Book
import pandas as pd
from objerver import observer
import logging
from decorators import log_function_call


class Library(observer):
    def __init__(self):
        self.messages_file = "messages.csv"
        self.ensure_file_exists(self.messages_file)
        self.books_file = "books.csv"
        self.book_obj = self.load_books_from_file_as_obj(self.books_file)
        self.loaned_books_file = "loaned_books.csv"
        self.available_books_file = "available_books.csv"
        #self.books_df = pd.read_csv("books.csv")  # ה-CSV כ- DataFrame
        self.users_file ="user.csv"
        self.books = self.get_all_book_titles()

    def ensure_file_exists(self, file_path):
        if not os.path.exists(file_path):
            with open(file_path, "w", newline='', encoding="utf-8") as file:
                file.write("username,message\n")
            print(f"File '{file_path}' created.")

    def get_first_waiting_person(self,book_title):
            with open("books.csv", "r", encoding='utf-8') as file:
                for line in file:
                    fields = line.strip().split(',')
                    if book_title in fields[0]:
                        if len(fields) > 6 and fields[6]:
                            first_person = fields[6].split('|')
                            return {
                                "name": first_person[0],
                                "phone": first_person[1],
                                "email": first_person[2]
                            }
                return None

    @log_function_call
    def add_global_message(self,message):
        try:
            users = []
            with open("user.csv", "r", encoding='utf-8') as file:
                for line in file:
                    username = line.strip().split(',')[0]
                    users.append(username)
            for username in users:
                with open("messages.csv", "a", encoding='utf-8') as file:
                    file.write(f"{username},{message}\n")

        except Exception as e:
            print(f"Error sending global message: {e}")

    def update(self,newsletter):
        self.add_global_message(newsletter)
    def update_is_loaned_books(self):
        print("updating is_loaned_books")
        try:
            with open(self.books_file, 'r') as original_file, open(self.loaned_books_file, 'w') as loaned_file:
                header = original_file.readline()
                loaned_file.write(header)
                for line in original_file:
                    fields = line.strip().split(',')
                    if fields[2].strip().lower() == 'yes':
                        loaned_file.write(line)
        except FileNotFoundError:
            print(f"Error: The file {self.books_file} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")
    def update_available_books(self):
        print("updating is_ava_books")
        with open(self.books_file, 'r') as original_file, open(self.available_books_file, 'w') as available_file:
            header = original_file.readline()
            available_file.write(header)
            for line in original_file:
                fields = line.strip().split(',')
                is_loaned = fields[2].strip()
                if is_loaned.lower() == 'no':
                    available_file.write(line)
    def load_books_from_file_as_obj(self,books_file):
        books_obj = []
        with open(books_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                book = Book(
                    title=row['title'],
                    author=row['author'],
                    is_loaned=row['is_loaned'],
                    copies=int(row['copies']),
                    genre=row['genre'],
                    year=int(row['year']),
                )
                books_obj.append(book)
        return books_obj
    @staticmethod
    def get_popular_books():
        input_file = "loaned_books.csv"
        output_file = "popular_list.csv"

        if not os.path.exists(input_file):
            print(f"Error: File '{input_file}' not found.")
            return

        try:
            with open(input_file, 'r', newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                books = []

                for row in reader:
                    if 'title' in row and 'copies' in row:

                        total_copies = int(row.get('copies', 0))

                        waiting_list = list(row.values())[6:]
                        if waiting_list:
                            total_copies += sum(1 for x in waiting_list if x and x.strip())

                        books.append({
                            "title": row.get('title', ''),
                            "author": row.get('author', ''),
                            "is_loaned": row.get('is_loaned', ''),
                            "copies": int(row.get('copies', 0)),
                            "total_copies": total_copies,
                            "genre": row.get('genre', ''),
                            "year": row.get('year', '')
                        })

                sorted_books = sorted(books, key=lambda x: x["total_copies"], reverse=True)

            with open(output_file, "w", newline='', encoding="utf-8") as popular_file:
                writer = csv.writer(popular_file)
                writer.writerow(["title", "author", "is_loaned", "copies", "total_copies", "genre", "year"])

                for book in sorted_books[:10]:
                    writer.writerow([
                        book["title"],
                        book["author"],
                        book["is_loaned"],
                        book["copies"],
                        book["total_copies"],
                        book["genre"],
                        book["year"]
                    ])

            print(f"Popular books written to '{output_file}'.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def get_all_book_titles(self):
        all_titles = []
        try:
            with open("available_books.csv", 'r', encoding='utf-8') as file:
                next(file)
                for line in file:
                    title = line.strip().split(',')[0]
                    all_titles.append(title)
        except FileNotFoundError:
            print("file not found")
        try:
            with open("loaned_books.csv", 'r', encoding='utf-8') as file:
                next(file)
                for line in file:
                    title = line.strip().split(',')[0]
                    all_titles.append(title)
        except FileNotFoundError:
            logging.error("This is an error message.")
            print("file not found")
        all_titles = sorted(list(set(all_titles)))
        return all_titles

    def add_book_to_file(self, title, author, is_loaned, copies, genre, year, file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()
            book_exists = False
            for i, line in enumerate(lines):
                fields = line.strip().split(',')
                if fields[0] == title:
                    fields[3] = str(int(fields[3]) + 1)
                    lines[i] = ','.join(fields) + '\n'
                    book_exists = True
                    break

        if book_exists:
            with open(file_name, 'w') as file:
                file.writelines(lines)
        else:
            new_book = Book(title, author, is_loaned, copies, genre, year)
            logging.debug(f"Book '{title}' added successfully.")
            with open(file_name, 'a') as file:
                file.write(str(new_book))

    def remove_book_from_file(self, file_name, title):
        updated_lines = []
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                fields = line.strip().split(',')
                print('this is title ' + title)
                print("this is my title " + fields[0])
                if str(fields[0]) == str(title):
                    current_copies = int(fields[3])
                    if current_copies - 1 > 0:
                        fields[3] = str(current_copies - 1)
                        updated_lines.append(','.join(fields) + '\n')
                else:
                    updated_lines.append(line)
        with open(file_name, 'w') as file:
            file.writelines(updated_lines)
        logging.debug(f"remove book {title} successfully")
    def remove_waiting_person_from_list(self, book_title):
        try:
            with open(self.books_file, 'r') as file:
                lines = file.readlines()

            updated_lines = []
            for i, line in enumerate(lines):
                if book_title in line:
                    if self.get_first_waiting_person(book_title) is not None:
                        new_line = line.split(",")
                        if len(new_line) > 6:
                            new_line = new_line[:6] + new_line[7:]
                            formatted_line = ",".join(new_line).strip()
                            updated_lines.append(formatted_line + "\n")
                            self.loan_book(book_title)
                        else:
                            updated_lines.append(line)
                    else:
                        print(f"No one is waiting for '{book_title}'.")
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)

            with open(self.books_file, 'w') as file:
                file.writelines(updated_lines)

        except FileNotFoundError:
            logging.error("This is an error message.")
            print(f"Error: Could not find {self.books_file}")
        except Exception as e:
            logging.error("This is an error message.")
            print(f"Error occurred while removing waiting person: {e}")

    @log_function_call
    def loan_book(self, book_title_partial):
        try:
            df = pd.read_csv(self.available_books_file)
            print(df)

            if 'title' not in df.columns:
                raise ValueError("The 'Title' column is missing from the available_books file.")
            matching_books = df[df['title'].str.contains(book_title_partial, case=False, na=False)]

            if not matching_books.empty:
                if len(matching_books) > 1:
                    print("Multiple matches found. Please specify:")
                    print(matching_books[['title', 'author']])
                    return False
                book = matching_books.iloc[0]
                self.remove_book_from_file(self.available_books_file, book['title'])
                self.add_book_to_file(book['title'], book['author'], "yes", 1, book['genre'], book['year'],
                                      self.loaned_books_file)
                first_waiting_person = self.get_first_waiting_person(book['title'])
                # print(first_waiting_person)
                # if first_waiting_person:
                #     self.remove_waiting_person_from_list(book['title'])
                #     self.update(f"the book {book['title']} is loaned to {first_waiting_person['name']}")
                return True
            else:
                print(f"No matching books found for '{book_title_partial}'.")
                return False

        except FileNotFoundError:
            print(f"Error: Could not find {self.available_books_file}")
            return False

    def chang_str_to_book(self,str):
        for book in self.book_obj:
            if book.get_title() == str:
                return book

    @log_function_call
    def return_book(self, str_book):
        print(str_book)
        loaned_books = pd.read_csv("loaned_books.csv")
        print(loaned_books)
        book_loaned = loaned_books[loaned_books['title'] == str_book]
        if book_loaned.empty:
            print(f"error: the book {str_book}is not loaned so you cant return it.")
            return False
        book = self.chang_str_to_book(str_book)
        self.add_book_to_file(book.get_title(), book.get_author(), "No", 1, book.get_genre(), book.get_year(),
                              self.available_books_file)
        self.remove_book_from_file(self.loaned_books_file, book.get_title())

        # print(first_waiting_person)
        # if first_waiting_person:

        self.remove_waiting_person_from_list(str_book)
        #     self.update(f"the book {book['title']} is loaned to {first_waiting_person['name']}")
        print(f"the book {str_book} returned successfully.")
        self.update(f"the book {str_book} is added to our library by {self.get_first_waiting_person(str_book)}")
        return True


    def add_book(self,book):
        self.add_book_to_file(book.get_title(), book.get_author(), "No", 1, book.get_genre(), book.get_year(),
                              "available_books.csv")
        self.update("new book is here")

    def get_messages_for_user(self, username):
        messages = []
        remaining_lines = []

        if os.path.exists("messages.csv"):
            with open("messages.csv", "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split(",", 1)
                    if len(parts) == 2:
                        if parts[0] == username:
                            messages.append(parts[1])
                        else:
                            remaining_lines.append(line)
        with open("messages.csv", "w", encoding="utf-8") as file:
            file.writelines(remaining_lines)
        return messages



    # def add_message(self, username, message):
    #     file_path = "messages.csv"
    #     try:
    #         if not os.path.exists(file_path):
    #             with open(file_path, "w", newline='', encoding="utf-8") as file:
    #                 file.write("username,message\n")  # כתיבת כותרות
    #         with open(file_path, "a", newline='', encoding="utf-8") as file:
    #             file.write(f"{username},{message}\n")
    #         print(f"Message '{message}' added for user '{username}'.")
    #     except Exception as e:
    #         logging.error("This is an error message.")
    #         print(f"Error writing message: {e}")

    def find_book_by_title(self,file_path, title):
        df = pd.read_csv(file_path)
        if title in df['title'].values:
            return False
        return True

    def remove_book(self, book_title, file_path):
        try:
            df = pd.read_csv(file_path)
            if book_title not in df['title'].values:
                return False
            df = df[df['title'] != book_title]
            df.to_csv(file_path, index=False)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"error: {str(e)}")
            return False

    def update_book(self, title, is_loaned, copies):
        with open("books.csv", 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                fields = line.strip().split(',')
                if fields[0] == title:
                    fields[3] = str(copies)
                    fields[2] = str(is_loaned)
                    lines[i] = ','.join(fields) + '\n'
                    break
        with open("books.csv", 'w') as file:
            file.writelines(lines)

    # def search_books(self, strategy, **filters):
    #     query = pd.Series(True, index=self.books_df.index)
    #     for column, value in filters.items():
    #         if column not in self.books_df.columns:
    #             raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    #         result = strategy.search(self.books_df, value)
    #         if isinstance(result, pd.DataFrame):
    #             result = result.iloc[:, 0]
    #         query &= result
    #     return self.books_df[query]
    logging.basicConfig(
        filename='logger_file.txt.log',  # The name of the log file
        level=logging.DEBUG,  # Minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s',  # Format of log messages
        filemode='a',  # Append mode ('w' overwrites the file)
        encoding='utf-8'  # Encoding for the log file
    )


if __name__ == '__main__':
    library = Library()
    # library.update_is_loaned_books()
    # library.update_available_books()
    GUI_Libarary.start_gui()
    Library.get_popular_books()
    # book= Book("Madame ","Gustave Flaubert","No","3","Realism","1857")
    # print(book)
    # library.add_book_to_file(book.get_title(), book.get_author(), book.get_is_loaned(), book.get_copies(),book.get_genre(),book.get_year(),"available_books.csv")
    # library.loan_book(book)
    # df = pd.read_csv('books.csv')
    # author_search=AuthorSearch()
    # result = search_books(df,author_search ,author="J.K. Rowling")
    # print(result)
    # loan_status_dict = create_loan_status_dict(df)
    # print(loan_status_dict)
    # library.ensure_messages_column_exists()