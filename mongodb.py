from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI
db = client["test"]  # Your database name
courses_collection = db["courses"]  # Your courses collection

def get_courses():
    # Fetch only non-expired courses
    courses = list(courses_collection.find({
        "$or": [
            {"expired": {"$exists": False}},
            {"expired": False}
        ]
    }).sort("Timestamp", -1))

    for course in courses:
        if 'Publication Date' in course:
            course['Publication Date'] = datetime.strptime(
                course['Publication Date'], "%a, %d %b %Y %H:%M:%S +%f"
            ).strftime("%Y-%m-%d %H:%M:%S")
    
    return courses


def get_course_by_id(course_id):
    course = courses_collection.find_one({"_id": ObjectId(course_id)})

    if course and 'Publication Date' in course:
        course['Publication Date'] = datetime.strptime(
            course['Publication Date'], "%a, %d %b %Y %H:%M:%S +%f"
        ).strftime("%Y-%m-%d %H:%M:%S")

    return course



def get_expired_courses():
    courses = list(courses_collection.find({"expired": True}).sort("Timestamp", -1))

    for course in courses:
        if 'Publication Date' in course:
            course['Publication Date'] = datetime.strptime(
                course['Publication Date'], "%a, %d %b %Y %H:%M:%S +%f"
            ).strftime("%Y-%m-%d %H:%M:%S")
    
    return courses
