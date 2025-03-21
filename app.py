from flask import Flask, render_template, jsonify
from mongodb import get_courses, get_course_by_id  # Import functions to get courses from MongoDB

app = Flask(__name__)  # Initialize the Flask application

# Route for the homepage (index page)
@app.route('/')
def home():
    return render_template('courses.html', courses=get_courses())  # This will render index.html when Home is clicked


@app.route('/home')
def index_page():
    return render_template('index.html')


@app.route('/courses', methods=['GET'])
def courses():
    all_courses = get_courses()
    return render_template('courses.html', courses=all_courses)

# Route to display details of a specific course
@app.route('/course/<course_id>', methods=['GET'])
def course_details(course_id):
    # Fetch the course details by course_id
    course = get_course_by_id(course_id)  # Assuming get_course_by_id is a function in mongodb.py
    return render_template('course_details.html', course=course)

# Route for the API to fetch courses in JSON format (for possible AJAX requests)
@app.route('/api/courses')
def api_courses():
    # Fetch courses and return them as JSON
    courses = get_courses()
    return jsonify(courses)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
