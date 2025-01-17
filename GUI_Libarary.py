import tkinter as tk
from tkinter import messagebox, ttk
import os
import hashlib
import pandas as pd
import search_strategies
from LibraryManager import Library
from Book import Book

current_username = None

root = tk.Tk()
library = Library()


def start_gui():
    root.title("Library")
    root.geometry("600x400")  # Smaller window size
    root.config(bg="#2C3E50")  # Dark gray background

    # Making the welcome label bigger and more stylish
    welcome_label = tk.Label(root, text="Welcome to the Library!", font=("Times New Roman", 28, "bold"), bg="#2C3E50",
                             fg="#ECF0F1")
    welcome_label.place(x=60, y=100)  # Adjusted position for better centering

    button_login = tk.Button(root, text="Log in", font=("Times New Roman", 14, "bold"), height=2, width=12,
                             command=log_in_action, bg="#3498DB", fg="white", relief="raised", bd=4)
    button_login.place(x=150, y=200)

    button_signup = tk.Button(root, text="Sign up", font=("Times New Roman", 14, "bold"), height=2, width=12,
                              command=sign_up_action, bg="#3498DB", fg="white", relief="raised", bd=4)
    button_signup.place(x=300, y=200)

    root.mainloop()


def hash_password(password):
    """Encrypt the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def open_waitlist_window(book_title):
    waitlist_window = tk.Toplevel(root)
    waitlist_window.title("enter to wait list file")
    waitlist_window.geometry("400x350")
    waitlist_window.config(bg="#F5F5F5")

    title_label = tk.Label(
        waitlist_window,
        text=f"the book{book_title}is not available please enter details of the person who wants to get in waitlist\n",
        font=("Helvetica", 12),
        bg="#F5F5F5"
    )
    title_label.pack(pady=15)

    fields = {}

    tk.Label(waitlist_window, text="name", font=("Times New Roman", 11), bg="#F5F5F5").pack(pady=5)
    fields["name"] = tk.Entry(waitlist_window, font=("Times New Roman", 11), width=25)
    fields["name"].pack(pady=5)

    tk.Label(waitlist_window, text="phone", font=("Times New Roman", 11), bg="#F5F5F5").pack(pady=5)
    fields["phone"] = tk.Entry(waitlist_window, font=("Times New Roman", 11), width=25)
    fields["phone"].pack(pady=5)

    tk.Label(waitlist_window, text="email", font=("Times New Roman", 11), bg="#F5F5F5").pack(pady=5)
    fields["email"] = tk.Entry(waitlist_window, font=("Times New Roman", 11), width=25)
    fields["email"].pack(pady=5)

    def submit_waitlist():
        if all(field.get() for field in fields.values()):
            try:
                with open("books.csv", "r") as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        if book_title in line:
                            waiting_info = f"{fields['name'].get()}|{fields['phone'].get()}|{fields['email'].get()},"
                            fields_list = line.strip().split(',')
                            fields_list[-1] = waiting_info + '\n'
                            lines[i] = ','.join(fields_list)
                            break

                with open("books.csv", "w") as file:
                    file.writelines(lines)

                messagebox.showinfo("success")
                waitlist_window.destroy()
            except Exception as e:
                messagebox.showerror("error", str(e))
        else:
            messagebox.showerror("error", "fill all fields")

    submit_button = tk.Button(
        waitlist_window,
        text="enter to waitlist",
        font=("Helvetica", 12),
        bg="#3498DB",
        fg="white",
        command=submit_waitlist
    )
    submit_button.pack(pady=20)


def open_loan_book_window():
    loan_book_window = tk.Toplevel(root)
    loan_book_window.title("Loan Book")
    loan_book_window.geometry("500x400")
    loan_book_window.config(bg="#F5F5F5")

    title_label = tk.Label(
        loan_book_window, text="Enter Book Title to Loan:", font=("Helvetica", 14),
        bg="#F5F5F5", fg="#2C3E50"
    )
    title_label.pack(pady=10)

    title_entry = tk.Entry(
        loan_book_window, font=("Times New Roman", 14), width=30, bg="#ECF0F1"
    )
    title_entry.pack(pady=10)

    suggestions_listbox = tk.Listbox(
        loan_book_window, font=("Times New Roman", 12), width=50, height=10, bg="#ECF0F1"
    )
    suggestions_listbox.pack(pady=10)

    def submit_loan_action():
        global current_username
        book_title = title_entry.get()
        if book_title:
            # try:
            if library.loan_book(book_title):
                print("true")
                messagebox.showinfo("Success", f"The book '{book_title}' has been successfully loaned!")
                loan_book_window.destroy()
            else:
                print("else")
                open_waitlist_window(book_title)
                # loan_book_window.destroy()
        # except Exception as e:
        #     messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please enter a valid book title.")

    submit_button = tk.Button(
        loan_book_window, text="lend Book", font=("Times New Roman", 14),
        bg="#3498DB", fg="white", command=submit_loan_action
    )
    submit_button.pack(pady=20)

    def update_suggestions(event):
        search_query = title_entry.get().lower()
        suggestions_listbox.delete(0, tk.END)
        all_books = library.books

        matching_books = [
            book for book in all_books if search_query.lower() in book.lower()
        ]

        for book in matching_books:
            suggestions_listbox.insert(tk.END, book)

    title_entry.bind("<KeyRelease>", update_suggestions)

    def select_suggestion(event):
        selected_book = suggestions_listbox.get(suggestions_listbox.curselection())
        title_entry.delete(0, tk.END)
        title_entry.insert(0, selected_book)

    suggestions_listbox.bind("<Double-Button-1>", select_suggestion)


def open_return_book_window():
    return_book_window = tk.Toplevel(root)
    return_book_window.title("return Book")
    return_book_window.geometry("500x400")
    return_book_window.config(bg="#F5F5F5")

    title_label = tk.Label(
        return_book_window, text="Enter Book Title to Return:", font=("Times New Roman", 14),
        bg="#F5F5F5", fg="#2C3E50"
    )
    title_label.pack(pady=10)

    title_entry = tk.Entry(
        return_book_window, font=("Times New Roman", 14), width=30, bg="#ECF0F1"
    )
    title_entry.pack(pady=10)

    suggestions_listbox = tk.Listbox(
        return_book_window, font=("Times New Roman", 12), width=50, height=10, bg="#ECF0F1"
    )
    suggestions_listbox.pack(pady=10)

    def update_suggestions(event):
        search_query = title_entry.get().lower()
        suggestions_listbox.delete(0, tk.END)

        all_books = library.books

        matching_books = [
            book for book in all_books if search_query.lower() in book.lower()
        ]

        for book in matching_books:
            suggestions_listbox.insert(tk.END, book)

    title_entry.bind("<KeyRelease>", update_suggestions)

    def select_suggestion(event):
        selected_book = suggestions_listbox.get(suggestions_listbox.curselection())
        title_entry.delete(0, tk.END)
        title_entry.insert(0, selected_book)

    suggestions_listbox.bind("<Double-Button-1>", select_suggestion)

    def submit_return_action():

        global current_username
        book_title = title_entry.get()
        if book_title:
            # try:
            book_return = library.return_book(book_title)
            if book_return:
                messagebox.showinfo("Success", f"The book '{book_title}' has been successfully returned!")
                return_book_window.destroy()
            else:
                messagebox.showerror("Error",
                                     "error: the book The Catcher in the Ryeis not loaned so you cant return it")
        # except Exception as e:
        # messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please enter a valid book title.")

    submit_button = tk.Button(
        return_book_window, text="Return Book", font=("Times New Roman", 14),
        bg="#3498DB", fg="white", command=submit_return_action
    )
    submit_button.pack(pady=20)


def open_remove_book_window():
    remove_book_window = tk.Toplevel(root)
    remove_book_window.title("return Book")
    remove_book_window.geometry("500x400")
    remove_book_window.config(bg="#F5F5F5")

    title_label = tk.Label(
        remove_book_window, text="Enter Book Title to Return:", font=("Times New Roman", 14),
        bg="#F5F5F5", fg="#2C3E50"
    )
    title_label.pack(pady=10)

    title_entry = tk.Entry(
        remove_book_window, font=("Times New Roman", 14), width=30, bg="#ECF0F1"
    )
    title_entry.pack(pady=10)

    suggestions_listbox = tk.Listbox(
        remove_book_window, font=("Times New Roman", 12), width=50, height=10, bg="#ECF0F1"
    )
    suggestions_listbox.pack(pady=10)

    def update_suggestions(event):
        search_query = title_entry.get().lower()
        suggestions_listbox.delete(0, tk.END)

        all_books = library.books

        matching_books = [
            book for book in all_books if search_query.lower() in book.lower()
        ]

        for book in matching_books:
            suggestions_listbox.insert(tk.END, book)

    title_entry.bind("<KeyRelease>", update_suggestions)

    def select_suggestion(event):
        selected_book = suggestions_listbox.get(suggestions_listbox.curselection())
        title_entry.delete(0, tk.END)
        title_entry.insert(0, selected_book)

    suggestions_listbox.bind("<Double-Button-1>", select_suggestion)

    def submit_remove_action():

        global current_username
        book_title = title_entry.get()
        if book_title:
            # try:
            remove_book = library.remove_book(book_title, "available_books.csv")
            if remove_book:
                messagebox.showinfo("Success", f"The book '{book_title}' has been successfully removed!")
                remove_book_window.destroy()
            else:
                messagebox.showerror("Error", f"error: the book {book_title} is loaned so you cant remove it")
        # except Exception as e:
        # messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please enter a valid book title.")

    submit_button = tk.Button(
        remove_book_window, text="Remove Book", font=("Times New Roman", 14),
        bg="#3498DB", fg="white", command=submit_remove_action
    )
    submit_button.pack(pady=20)


def add_user(username, password):
    encrypted_password = hash_password(password)
    if os.path.exists("user.csv"):
        with open("user.csv", "r") as file:
            users = [line.strip().split(",")[0] for line in file]
            if username in users:
                raise ValueError("Username already exists.")
    with open("user.csv", "a") as file:
        file.write(f"{username},{encrypted_password}\n")


def open_add_book_window():
    add_book_window = tk.Toplevel(root)
    add_book_window.title("Add Book")
    add_book_window.geometry("400x600")
    add_book_window.config(bg="#F5F5F5")

    title_label = tk.Label(add_book_window, text="Add New Book", font=("Times New Roman", 18, "bold"), bg="#F5F5F5",
                           fg="#2C3E50")
    title_label.pack(pady=10)

    fields = ["Title", "Author", "Is Loaned (Yes/No)", "Copies", "Genre", "Year"]
    entries = {}

    for field in fields:
        label = tk.Label(add_book_window, text=f"{field}:", font=("Times New Roman", 14), bg="#F5F5F5", fg="#2C3E50")
        label.pack(pady=5)
        entry = tk.Entry(add_book_window, font=("Times New Roman", 14), width=25, bg="#ECF0F1")
        entry.pack(pady=5)
        entries[field] = entry

    def save_book():
        title = entries["title"].get()
        author = entries["author"].get()
        is_loaned = entries["Is Loaned (Yes/No)"].get().strip().lower() == "yes"
        copies = entries["copies"].get()
        genre = entries["genre"].get()
        year = entries["year"].get()

        if not (title and author and copies.isdigit() and genre and year.isdigit()):
            messagebox.showerror("Error", "Please fill in all fields correctly.")
            return
        try:
            book = Book(title, author, is_loaned, int(copies), genre, int(year))
            library.add_book(book)
            messagebox.showinfo("Success", "Book added successfully!")
            add_book_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    submit_button = tk.Button(add_book_window, text="Add Book", font=("Times New Roman", 14), bg="#3498DB", fg="white",
                              command=save_book)
    submit_button.pack(pady=20)


def open_popular_books():
    window = tk.Toplevel()
    window.title("Popular Books")
    window.geometry("900x600")
    window.configure(bg="#AAB8C2")

    tk.Label(
        window,
        text="Popular Books",
        font=("Times New Roman", 20),
        bg="#AAB8C2",
        fg="#FFFFFF"
    ).pack(pady=10)

    tree = ttk.Treeview(window)
    tree.pack(fill='both', expand=True, padx=10, pady=10)

    try:
        Library.get_popular_books()
        popular_books = pd.read_csv("popular_list.csv")
        columns = list(popular_books.columns)

        tree["columns"] = columns
        tree["show"] = "headings"

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center", width=100)

        for _, row in popular_books.iterrows():
            tree.insert("", "end", values=list(row))

    except FileNotFoundError:

        tk.Label(
            window,
            text="No books found!",
            bg="#AAB8C2",
            fg="red",
            font=("Arial", 14)
        ).pack(pady=20)

    tk.Button(
        window,
        text="Close",
        font=("Times New Roman", 15),
        bg="#3498DB",
        fg="#FFFFFF",
        command=window.destroy
    ).pack(pady=10)


def open_library_window():
    library_window = tk.Toplevel(root)
    library_window.title("Library Management")
    library_window.geometry("500x400")
    library_window.config(bg="#F5F5F5")

    title_label = tk.Label(library_window, text="Library Management", font=("Times New Roman", 20, "bold"),
                           bg="#F5F5F5", fg="#2C3E50")
    title_label.pack(pady=20)

    tk.Button(library_window, text="Return Book", command=open_return_book_window).pack(pady=10)
    tk.Button(library_window, text="Add Book", command=open_add_book_window).pack(pady=10)
    tk.Button(library_window, text="Remove Book", command=open_remove_book_window).pack(pady=10)
    tk.Button(library_window, text="lend Book", command=open_loan_book_window).pack(pady=10)
    tk.Button(library_window, text="Search Book", command=open_search_window).pack(pady=10)
    tk.Button(library_window, text="view books", command=show_all_system_books).pack(pady=10)
    tk.Button(library_window, text="popular books", command=open_popular_books).pack(pady=10)
    tk.Button(library_window, text="log out", command=logout).pack(pady=10)


    root.withdraw()


def get_messages(username):
    messages = []
    if os.path.exists("messages.csv"):
        with open("messages.csv", "r") as file:
            for line in file:
                stored_username, stored_messages = line.strip().split(",", 1)
                if stored_username == username:
                    messages = stored_messages.split("|")
                    break
    return messages


def show_login_message(username):
    messages = library.get_messages_for_user(username)
    if messages:
        message_window = tk.Toplevel(root)
        message_window.title("new messages")
        message_window.geometry("400x300")
        message_window.config(bg="#F5F5F5")

        for msg in messages:
            message_label = tk.Label(
                message_window,
                text=msg,
                font=("Times New Roman", 12),
                bg="#F5F5F5"
            )
            message_label.pack(pady=10)
        message_window.after(10000, message_window.destroy)


def check_user(username, password, password_window):
    encrypted_password = hash_password(password)
    if not os.path.exists("user.csv"):
        return False
    with open("user.csv", "r") as file:
        for line in file:
            stored_username, stored_encrypted_password = line.strip().split(",")
            if stored_username == username and stored_encrypted_password == encrypted_password:
                show_login_message(username)
                password_window.destroy()
                return True
    return False

def open_password_window(action):
    password_window = tk.Toplevel(root)
    password_window.title(action)
    password_window.geometry("350x250")  # Smaller window size
    password_window.config(bg="#BDC3C7")  # Light gray background

    username_label = tk.Label(password_window, text="Enter username:", font=("Times New Roman", 14), bg="#BDC3C7",
                              fg="#2C3E50")
    username_label.pack(pady=10)

    username_entry = tk.Entry(password_window, font=("Times New Roman", 14), bg="#ECF0F1", width=20, bd=2,
                              relief="solid")
    username_entry.pack(pady=10)

    password_label = tk.Label(password_window, text="Enter password:", font=("Times New Roman", 14), bg="#BDC3C7",
                              fg="#2C3E50")
    password_label.pack(pady=10)

    password_entry = tk.Entry(password_window, font=("Times New Roman", 14), show="*", bg="#ECF0F1", width=20, bd=2,
                              relief="solid")
    password_entry.pack(pady=10)

    def submit_action():
        global current_username
        username = username_entry.get()
        password = password_entry.get()

        if action == "Log in":
            if check_user(username, password, password_window):
                current_username = username
                messagebox.showinfo("Success", "Logged in successfully!")
                # password_window.withdraw()
                # root.destroy()
                open_library_window()
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        elif action == "Sign up":
            try:
                add_user(username, password)
                messagebox.showinfo("Success", "User sign up successfully!")
                password_window.withdraw()
                # root.destroy()
                open_library_window()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    submit_button = tk.Button(password_window, text="Submit", font=("Times New Roman", 14), width=7, height=5,
                              bg="#3498DB", fg="white",
                              command=submit_action, relief="raised", bd=4)
    submit_button.pack(pady=20)


def open_search_window():
    search_window = tk.Toplevel(root)
    search_window.title("Search Book")
    search_window.geometry("400x300")
    search_window.configure(bg="#AAB8C2")
    tk.Label(search_window, text="Search Book", font=("Times New Roman", 20), bg="#AAB8C2", fg="#FFFFFF").pack(pady=10)
    tk.Label(search_window, text="Select Criterion:", font=("Times New Roman", 15), bg="#AAB8C2", fg="#2C3E50").pack(pady=5)
    criterion_var = tk.StringVar(value="title")
    tk.OptionMenu(search_window, criterion_var, "title", "author", "genre", "year").pack()
    tk.Label(search_window, text="Enter Query:", font=("Times New Roman", 15), bg="#AAB8C2", fg="#2C3E50").pack(pady=5)
    search_entry = tk.Entry(search_window, font=("Times New Roman", 15))
    search_entry.pack(pady=5)

    def execute_search():
        query = search_entry.get()
        criterion = criterion_var.get()
        print(criterion)
        results = search_strategies.search_books(criterion, query)

        result_window = tk.Toplevel(search_window)
        result_window.title("Search Results")
        result_window.geometry("600x400")
        result_window.configure(bg="#AAB8C2")
        tk.Label(result_window, text="Search Results", font=("Times New Roman", 20), bg="#AAB8C2", fg="#FFFFFF").pack(pady=10)
        columns = ["Title", "Author", "Is Loaned", "Copies", "Genre", "Year"]
        tree = ttk.Treeview(result_window, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)
        tree.pack(pady=10, fill="both", expand=True)
        if results is not None and not results.empty:
            for _, row in results.iterrows():
                tree.insert("", "end", values=row.tolist())
        else:
            tk.Label(result_window, text="No results found!", font=("Times New Roman", 15), bg="#AAB8C2",
                     fg="red").pack(pady=10)

        tk.Button(result_window, text="Close", font=("Times New Roman", 15), bg="#AAB8C2", fg="#3498DB",
                  command=result_window.destroy).pack(pady=10)

    tk.Button(search_window, text="Search", font=("Times New Roman", 15), bg="#AAB8C2", fg="#2C3E50",
              command=execute_search).pack(pady=10)

    tk.Button(search_window, text="Close", font=("Times New Roman", 15), bg="#AAB8C2", fg="#2C3E50",
              command=search_window.destroy).pack(pady=10)


def show_all_system_books():
    window = tk.Toplevel()
    window.title("all books")
    window.geometry("900x600")
    window.configure(bg="#3D2B1F")

    tree = ttk.Treeview(window)
    tree.pack(fill='both', expand=True, padx=10, pady=10)

    try:
        available_books = pd.read_csv("available_books.csv")
        loaned_books = pd.read_csv("loaned_books.csv")
        available_books['status'] = 'available'
        loaned_books['status'] = 'loaned'

        all_books = pd.concat([available_books, loaned_books], ignore_index=True)

        columns = list(all_books.columns)
        tree["columns"] = columns
        tree["show"] = "headings"

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=100)

        for _, row in all_books.iterrows():
            tree.insert("", "end", values=list(row))

    except FileNotFoundError:
        label = tk.Label(window,
                         text="no books found",
                         bg="#3D2B1F",
                         fg="#3498DB",
                         font=("Arial", 14))
        label.pack(pady=20)


def logout():
    if tk.messagebox.askokcancel("log out", "Are you sure you want to log out?"):
        for window in root.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.destroy()
        try:
            current_user = None
        except:
            pass
        root.deiconify()

def log_in_action():
    open_password_window("Log in")


def sign_up_action():
    open_password_window("Sign up")
