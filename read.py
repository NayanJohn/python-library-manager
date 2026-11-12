import json


with open("library.json", "r") as file:
    library = json.load(file)
    print(library)
    print(type(library))

with open("student.json", "r") as file:
    student = json.load(file)
    print(student)
    print(type(student))    

with open("issued.json", "r") as file:
    issued = json.load(file)
    print(issued)
    print(type(issued))