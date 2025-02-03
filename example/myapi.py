from fastapi import FastAPI ,Path 
from typing import Optional 
from pydantic import BaseModel  # Import Pydantic's BaseModel



app =FastAPI()

# amazon.com/create-User()


# GET - get an information 

# POST -create something new 

# PUT - update 

# DELETE - delete something 


@app.get("/")
def home():
    return {"name " : "first data "}


# Define a Pydantic model for the student
class Student(BaseModel):
    name: str
    age: int
    class_name: str  # Changed "class" to "class_name" to avoid conflict with the reserved keyword

students ={
    1:{
        "name":"senthil",
        "age":17,
        "class_name":"year 12"

    }

}


@app.get("/get-students/{student_id}")
def get_students(student_id: int = Path(..., description="the id of the student you want to view"),gt=0 ,lt=3):
    return students[student_id]


@app.get("/get-by-name")
def get_student(*, name: Optional[str] = None , test :int):
    for student_id in students:
        if students[student_id]["name"]==name:
            return students[student_id]
    return {"data":"Not Found"}



@app.post("/create-students/{student_id}")
def create_student(student_id: int, student: Student):  # Use the Student model here
    if student_id in students:
        return {"error": "student exists"}
    students[student_id] = student.model_dump()  # Use model_dump instead of dict
    return students[student_id]

