import json

library = {
    11097:{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "issued": False},
}
student ={
    "AI0945": {"name": "Bittu", "issued_books": []},

}
with open("library.json", "w") as file:
    json.dump(library, file)

with open("student.json", "w") as file:
    json.dump(student, file)

with open("issued_books.json", "w") as file:
    json.dump({}, file)

print("Library and student data saved to JSON files.")    
