import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from typing import Dict, Coroutine, List, Any,Optional
from bson.objectid import ObjectId
from pymongo.results import InsertOneResult,UpdateResult

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database: AsyncIOMotorDatabase = client.students
student_collection: AsyncIOMotorCollection = database.get_collection("students_collection")


# helpers

def student_helper(student: Dict) -> Dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }


# Retrieve all students present in the database
async def retrieve_students() -> Coroutine:
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))

    return students


# Add a new student into to the database
async def add_student(student_data: Dict) -> Coroutine:
    student: InsertOneResult = await student_collection.insert_one(student_data)
    new_student: Dict = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


# Retrieve a student with a matching ID
async def retrieve_student(id: str) -> Coroutine:
    student: Optional[Dict] = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


# Update a student with a matching ID
async def update_student(id: str, data: Dict) -> Coroutine:
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student: Optional[Dict] = await student_collection.find_one({"_id": ObjectId(id)})
    print(type(student))
    if student:
        updated_student: UpdateResult = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        print("updated student is of type ", type(updated_student))
        if updated_student:
            return True
        return False


# Delete a student from the database
async def delete_student(id: str) -> Coroutine:
    student: Optional[Dict] = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True


