from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI
db = client["test"]  # Your database name
courses_collection = db["courses"]  # Your courses collection

def get_courses(page=1, per_page=12, search=None):
    skip = (page - 1) * per_page

    query = {
        "$or": [{"expired": {"$exists": False}}, {"expired": False}]
    }

    if search:
        query["$and"] = [{
            "$or": [
                {"Title": {"$regex": search, "$options": "i"}},
                {"Category": {"$regex": search, "$options": "i"}}
            ]
        }]

    cursor = courses_collection.find(query).sort("Timestamp", -1).skip(skip).limit(per_page)
    courses = list(cursor)

    for course in courses:
        if 'Publication Date' in course:
            course['Publication Date'] = datetime.strptime(
                course['Publication Date'], "%a, %d %b %Y %H:%M:%S +%f"
            ).strftime("%Y-%m-%d %H:%M:%S")

    total = courses_collection.count_documents(query)
    return courses, total




def get_course_by_id(course_id):
    course = courses_collection.find_one({"_id": ObjectId(course_id)})

    if course and 'Publication Date' in course:
        course['Publication Date'] = datetime.strptime(
            course['Publication Date'], "%a, %d %b %Y %H:%M:%S +%f"
        ).strftime("%Y-%m-%d %H:%M:%S")

    return course



def get_expired_courses(page=1, per_page=12):
    skip = (page - 1) * per_page
    cursor = courses_collection.find({"expired": True}).sort("Timestamp", -1).skip(skip).limit(per_page)
    courses = list(cursor)

    for course in courses:
        if 'Publication Date' in course:
            course['Publication Date'] = datetime.strptime(
                course['Publication Date'], "%a, %d %b %Y %H:%M:%S +%f"
            ).strftime("%Y-%m-%d %H:%M:%S")

    total = courses_collection.count_documents({"expired": True})

    return courses, total

