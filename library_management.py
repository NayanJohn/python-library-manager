
import json
from datetime import date, timedelta

FILE_NAME="library.json"
FILE_NAME_STUDENT="student.json"
FILE_NAME_ISSUED="issued_books.json"

def load_data():
    with open(FILE_NAME, "r") as f:
        books = json.load(f)

    with open(FILE_NAME_STUDENT, "r") as f:
        student = json.load(f)

    with open(FILE_NAME_ISSUED, "r") as f:
        issued_data = json.load(f)

    return books, student, issued_data

def find_book(book_no):
    books, _, _ = load_data()
    return books.get(book_no)

def add_book():
    books,_, _  =load_data()
    book_no = input("Enter book number: ")
    if book_no == "":
        print("Book number cannot be empty.")
        return
    elif len(book_no)!=5:
        print("invalid Book number")
        return
    if find_book(book_no):
        print("Book already exists.")
        return
    title = input("Enter book title: ").strip()
    if title == "":
        print("Book title cannot be empty.")
        return
    author=input("Enter book author:").strip()
    if author=="":
        print("Book author cannot be empty.")
        return
    
    same_books = [
        n for n, b in books.items()
        if b["title"].lower() == title.lower() and b["author"].lower() == author.lower()
    ]

    copies = len(same_books) + 1   

    books[book_no] = {
        "title": title,
        "author": author,
        "issued": False,
        "copies": copies
    }

    for n in same_books:
        books[n]["copies"] = copies
    with open(FILE_NAME, "w") as f:
        json.dump(books, f, indent=4)
        print("Book added successfully")

def display_books():
    books, _, _ = load_data()
    if len(books) == 0:
        print("No books in the library.")
        return
    print("Books in the library:")


    for book_no, book_info in books.items():
            print(f"Book Number: {book_no}")
            print(f"Title: {book_info['title']}")
            print(f"Author: {book_info['author']}")
            print(f"Copies: {book_info.get('copies', 1)}")
            print()



def issue_book():
    books, student, issued_data = load_data()

    student_id = input("Enter student ID: ").strip()

    if student_id not in student:
        print("Student not found.")
        return

    book_no = input("Enter book number to issue: ").strip()

    book = books.get(book_no)

    if not book:
        print("Book not found.")
        return

    if book.get("issued", False):
        print("Book is already issued.")
        return

    issue_date = date.today().isoformat()
    due_date = (date.today() + timedelta(days=14)).isoformat()

    book["issued"] = True
    book["date_issued"] = issue_date
    book["due_date"] = due_date
    book["issued_to"] = student_id

    if "issued_books" not in student[student_id]:
        student[student_id]["issued_books"] = []

    student[student_id]["issued_books"].append(book_no)

    with open(FILE_NAME, "w") as f:
        json.dump(books, f, indent=4)

    with open(FILE_NAME_STUDENT, "w") as f:
        json.dump(student, f, indent=4)

    

    issued_data[book_no] = {
        "title": book["title"],
        "author": book["author"],
        "student_id": student_id,
        "student_name": student[student_id]["name"],
        "date_issued": issue_date,
        "due_date": due_date
    }

    with open(FILE_NAME_ISSUED, "w") as f:
        json.dump(issued_data, f, indent=4)

    print(f"Book'{book['title']}' issued successfully")

    


def return_book():
    books, student, issued_data = load_data()

    student_id = input("Enter student ID: ").strip()

    if student_id not in student:
        print("Student not found.")
        return

    book_no = input("Enter book number to return: ").strip()

    book = books.get(book_no)

    if not book:
        print("Book not found.")
        return

    if not book.get("issued", False):
        print("Book is not issued.")
        return

    if book.get("issued_to") != student_id:
        print("This book was not issued to this student.")
        return

    book["issued"] = False
    book.pop("date_issued", None)
    book.pop("due_date", None)
    book.pop("issued_to", None)

    issued_books = student[student_id].get("issued_books", [])

    if book_no in issued_books:
        issued_books.remove(book_no)

    issued_data.pop(book_no, None)    

    with open(FILE_NAME, "w") as f:
        json.dump(books, f, indent=4)

    with open(FILE_NAME_STUDENT, "w") as f:
        json.dump(student, f, indent=4)

    with open(FILE_NAME_ISSUED, "w") as f:
        json.dump(issued_data, f, indent=4)

    print(f"Book '{book['title']}' returned successfully.")

    

    with open(FILE_NAME_ISSUED, "w") as f:
        json.dump(issued_data, f, indent=4) 
    print(f"Book '{book['title']}' returned successfully.")




def available_books():
    books, _, _ = load_data()
    available = {book_no: info for book_no, info in  books.items() if not info.get("issued", False)}
    if not available:
        print("No available books.")
        return
    print("Available books:")
    for book_no, book_info in available.items():
        print(f"Book Number: {book_no}")
        print(f"Title: {book_info['title']}")
        print(f"Author: {book_info['author']}")
        print()

def issued_books():
    _, _, issued_data = load_data()
    if not issued_data:
        print("No issued books.")
        return
    print("Issued books:")
    for book_no, book_info in issued_data.items():
        print(f"Book Number: {book_no}")
        print(f"Title: {book_info['title']}")
        print(f"Author: {book_info['author']}")
        print(f"date issued: {book_info.get('date_issued', 'N/A')}")
        print(f"due date: {book_info.get('due_date', 'N/A')}")
        print()

def search_book():
    books, _, _  = load_data()
    title = input("Enter book title to search: ").strip()
    found = {n: b for n, b in books.items() if b.get("title", "").lower() == title.lower()}
    if not found:
        print("Book not found.")
        return
    groups = {}
    for n, b in found.items():
        key = (b["title"], b["author"])
        groups.setdefault(key, []).append((n, b))

    print("Search Results:")
    for (t, a), copies in groups.items():
        issued = [n for n, b in copies if b.get("issued", False)]
        available = [n for n, b in copies if not b.get("issued", False)]

        print(f"Title: {t}")
        print(f"Author: {a}")
        print(f"Total copies: {len(copies)}")
        print(f"Issued copies: {len(issued)} -> Book No: {', '.join(issued) if issued else 'None'}")
        print(f"Available copies: {len(available)} -> Book No: {', '.join(available) if available else 'None'}")
        print()
        
def student_registration():
    _, student, _ = load_data()
    student_id = input("Enter student ID: ").strip()
    if student_id in student:
        print("Student already registered.")
        return
    name = input("Enter student name: ").strip()
    if name == "":
        print("Student name cannot be empty.")
        return
    student[student_id] = {"name": name}
    with open(FILE_NAME_STUDENT, "w") as f:
        json.dump(student, f, indent=4)
    print("Student registered successfully.")

def student_account():
    _, student, _ = load_data()
    student_id = input("Enter student ID: ").strip()
    if student_id not in student:
        print("Student not found.")
        return
    print(f"Student ID: {student_id}")
    print(f"Name: {student[student_id]['name']}")
    print("Issued Books:")
    for book_no in student[student_id].get("issued_books", []):
        book = find_book(book_no)
        if book:
            print(f"Book Number: {book_no}")
            print(f"Title: {book['title']}")
            print(f"Author: {book['author']}")
            print(f"date issued: {book.get('date_issued', 'N/A')}")
            print(f"due date: {book.get('due_date', 'N/A')}")
            print()

def delete_book():
    books, _, _ = load_data()
    book_no = input("Enter book number to delete: ").strip()
    if book_no not in books:
        print("Book not found.")
        return
    if books[book_no].get("issued", False):
        print("Cannot delete an issued book.")
        return 
    del books[book_no]
    with open(FILE_NAME, "w") as f:
        json.dump(books, f, indent=4)
    print(f"Book '{book_no}' deleted successfully.")

def main():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Display Books")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Available Books")
        print("6. Issued Books")
        print("7. Search Book")
        print("8. Student Registration")
        print("9. Student Account")
        print("10. Delete Book")
        print("11. Exit")

        choice = input("Enter your choice (1-11): ")

        if choice == "1":
            add_book()
        elif choice == "2":
            display_books()
        elif choice == "3":
            issue_book()
        elif choice == "4":
            return_book()
        elif choice == "5":
            available_books()
        elif choice == "6":
            issued_books()
        elif choice == "7":
            search_book()
        elif choice == "8":
            student_registration()
        elif choice == "9":
            student_account()
        elif choice == "10":
            delete_book()
        elif choice == "11":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

main()