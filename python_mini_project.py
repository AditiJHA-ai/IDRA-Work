import csv
import os
from datetime import datetime


class Book:

    def __init__(self, book_id, title, author, genre, is_issued=False):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.is_issued = is_issued

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "is_issued": str(self.is_issued),
        }


class Member:

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []

    def to_dict(self):
        borrowed_str = ";".join(self.borrowed_books)
        return {
            "member_id": self.member_id,
            "name": self.name,
            "borrowed_books": borrowed_str,
        }


class LibrarySystem:

    def __init__(
        self,
        books_file="books.csv",
        members_file="members.csv",
        log_file="transactions.txt",
    ):
        self.books_file = books_file
        self.members_file = members_file
        self.log_file = log_file

        self.books = {}
        self.members = {}
        self.unique_genres = set()
        self.transactions = []

        self.load_data()

    def load_data(self):
        if os.path.exists(self.books_file):
            try:
                with open(
                    self.books_file, mode="r", newline="", encoding="utf-8"
                ) as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        is_issued = row["is_issued"].lower() == "true"
                        book = Book(
                            row["book_id"],
                            row["title"],
                            row["author"],
                            row["genre"],
                            is_issued,
                        )
                        self.books[book.book_id] = book
                        self.unique_genres.add(book.genre)
            except Exception as e:
                print(f"Error loading books file: {e}")

        if os.path.exists(self.members_file):
            try:
                with open(
                    self.members_file, mode="r", newline="", encoding="utf-8"
                ) as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        member = Member(row["member_id"], row["name"])
                        if row["borrowed_books"]:
                            member.borrowed_books = row["borrowed_books"].split(
                                ";"
                            )
                        self.members[member.member_id] = member
            except Exception as e:
                print(f"Error loading members file: {e}")

    def save_data(self):
        try:
            with open(
                self.books_file, mode="w", newline="", encoding="utf-8"
            ) as f:
                fieldnames = [
                    "book_id",
                    "title",
                    "author",
                    "genre",
                    "is_issued",
                ]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for book in self.books.values():
                    writer.writerow(book.to_dict())

            with open(
                self.members_file, mode="w", newline="", encoding="utf-8"
            ) as f:
                fieldnames = ["member_id", "name", "borrowed_books"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for member in self.members.values():
                    writer.writerow(member.to_dict())

        except IOError as e:
            print(f"Error saving data to disk: {e}")

    def log_transaction(self, action, book_id, member_id):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (timestamp, action, book_id, member_id)
        self.transactions.append(log_entry)

        try:
            with open(self.log_file, mode="a", encoding="utf-8") as f:
                f.write(
                    f"[{timestamp}] ACTION: {action} | BOOK_ID: {book_id} | MEMBER_ID: {member_id}\n"
                )
        except IOError as e:
            print(f"Failed to record transaction log: {e}")

    def add_book(self):
        print("\nAdd New Book")
        book_id = input("Enter Book ID: ").strip()
        if not book_id:
            print("Book ID cannot be empty.")
            return

        if book_id in self.books:
            print(f"A book with ID '{book_id}' already exists.")
            return

        title = input("Enter Book Title: ").strip()
        author = input("Enter Author Name: ").strip()
        genre = input("Enter Genre: ").strip().capitalize()

        if not title or not author or not genre:
            print("All fields are required.")
            return

        new_book = Book(book_id, title, author, genre)
        self.books[book_id] = new_book
        self.unique_genres.add(genre)
        self.save_data()
        print(f"Book '{title}' added successfully.")

    def register_member(self):
        print("\nRegister New Member")
        member_id = input("Enter Member ID: ").strip()
        if not member_id:
            print("Member ID cannot be empty.")
            return

        if member_id in self.members:
            print(f"Member with ID '{member_id}' is already registered.")
            return

        name = input("Enter Member Name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return

        new_member = Member(member_id, name)
        self.members[member_id] = new_member
        self.save_data()
        print(f"Member '{name}' registered successfully.")

    def view_all_books(self):
        print("\nLibrary Book Inventory")
        if not self.books:
            print("No books available in the inventory.")
            return

        print(
            f"{'ID':<10} | {'Title':<25} | {'Author':<20} | {'Genre':<15} | {'Status'}"
        )

        for book in self.books.values():
            status = "Issued" if book.is_issued else "Available"
            print(
                f"{book.book_id:<10} | {book.title:<25} | {book.author:<20} | {book.genre:<15} | {status}"
            )

    def view_all_members(self):
        print("\nRegistered Members")
        if not self.members:
            print("No members registered.")
            return

        print(f"{'Member ID':<12} | {'Name':<25} | {'Borrowed Books'}")

        for member in self.members.values():
            borrowed = (
                ", ".join(member.borrowed_books)
                if member.borrowed_books
                else "None"
            )
            print(f"{member.member_id:<12} | {member.name:<25} | {borrowed}")

    def issue_book(self):
        print("\nIssue Book")
        book_id = input("Enter Book ID: ").strip()
        if book_id not in self.books:
            print(f"Book ID '{book_id}' not found.")
            return

        book = self.books[book_id]
        if book.is_issued:
            print(f"Book '{book.title}' is currently issued to another member.")
            return

        member_id = input("Enter Member ID: ").strip()
        if member_id not in self.members:
            print(f"Member ID '{member_id}' not found.")
            return

        member = self.members[member_id]

        book.is_issued = True
        member.borrowed_books.append(book_id)

        self.save_data()
        self.log_transaction("ISSUE", book_id, member_id)
        print(f"Book '{book.title}' issued to '{member.name}' successfully.")

    def return_book(self):
        print("\nReturn Book")
        book_id = input("Enter Book ID to return: ").strip()
        if book_id not in self.books:
            print(f"Book ID '{book_id}' not found.")
            return

        book = self.books[book_id]
        if not book.is_issued:
            print(f"Book '{book.title}' is not currently marked as issued.")
            return

        member_id = input("Enter Member ID: ").strip()
        if member_id not in self.members:
            print(f"Member ID '{member_id}' not found.")
            return

        member = self.members[member_id]
        if book_id in member.borrowed_books:
            member.borrowed_books.remove(book_id)

        book.is_issued = False

        self.save_data()
        self.log_transaction("RETURN", book_id, member_id)
        print(f"Book '{book.title}' returned successfully.")

    def search_books(self):
        print("\nSearch Books")
        query = input("Enter Book Title, Author, or Genre: ").strip().lower()
        if not query:
            print("Search query cannot be empty.")
            return

        results = [
            b
            for b in self.books.values()
            if query in b.title.lower()
            or query in b.author.lower()
            or query in b.genre.lower()
        ]

        if not results:
            print(f"No books found matching '{query}'.")
            return

        print(
            f"\nFound {len(results)} match(es):\n"
            f"{'ID':<10} | {'Title':<25} | {'Author':<20} | {'Genre':<15} | {'Status'}"
        )

        for book in results:
            status = "Issued" if book.is_issued else "Available"
            print(
                f"{book.book_id:<10} | {book.title:<25} | {book.author:<20} | {book.genre:<15} | {status}"
            )

    def display_genres(self):
        print("\nAvailable Categories/Genres")
        if not self.unique_genres:
            print("No genres registered yet.")
            return
        for idx, genre in enumerate(sorted(self.unique_genres), 1):
            print(f"{idx}. {genre}")


def main():
    library = LibrarySystem()

    while True:
        print("\nLIBRARY MANAGEMENT SYSTEM")
        print("1. Add New Book")
        print("2. Register New Member")
        print("3. View All Books")
        print("4. View All Members")
        print("5. Issue Book")
        print("6. Return Book")
        print("7. Search Books")
        print("8. Display Available Genres")
        print("9. Exit")

        choice = input("Enter choice (1-9): ").strip()

        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.register_member()
        elif choice == "3":
            library.view_all_books()
        elif choice == "4":
            library.view_all_members()
        elif choice == "5":
            library.issue_book()
        elif choice == "6":
            library.return_book()
        elif choice == "7":
            library.search_books()
        elif choice == "8":
            library.display_genres()
        elif choice == "9":
            print("\nExiting Library Management System. Goodbye!")
            break
        else:
            print("Invalid selection. Please enter a choice between 1 and 9.")


if __name__ == "__main__":
    main()
