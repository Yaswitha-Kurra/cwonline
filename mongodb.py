from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# MongoDB connection setup
client = MongoClient("mongodb+srv://yaswitha:Microtek123%40@cluster0.m06cm.mongodb.net/")  # Update with your MongoDB URI
db = client["test"]  # Your database name
courses_collection = db["courses"]  # Your courses collection

def get_courses():
    # Fetch all courses from the MongoDB database
    courses = list(courses_collection.find({}))  # Converts the cursor to a list of courses

    # Convert date strings to a proper date format
    for course in courses:
        if 'Publication Date' in course:
            course['Publication Date'] = datetime.strptime(course['Publication Date'], "%a, %d %b %Y %H:%M:%S +%f").strftime("%Y-%m-%d %H:%M:%S")
    
    return courses


def get_course_by_id(course_id):
    # Fetch a single course by its ObjectId
    course = courses_collection.find_one({"_id": ObjectId(course_id)})

    # Convert the publication date if it exists
    if 'Publication Date' in course:
        course['Publication Date'] = datetime.strptime(course['Publication Date'], "%a, %d %b %Y %H:%M:%S +%f").strftime("%Y-%m-%d %H:%M:%S")
    
    return course
