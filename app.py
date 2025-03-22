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
@app.route('/course/<course_id>')
def course_details(course_id):
    course = get_course_by_id(course_id)
    if course is None:
        return render_template('courses.html')

    expired = course.get('expired', False)
    return render_template('course_details.html', course=course, expired=expired)


# Route for the API to fetch courses in JSON format (for possible AJAX requests)
@app.route('/api/courses')
def api_courses():
    # Fetch courses and return them as JSON
    courses = get_courses()
    return jsonify(courses)

@app.route('/expired', methods=['GET'])
def expired_courses():
    from mongodb import get_expired_courses
    courses = get_expired_courses()
    return render_template('expired_courses.html', courses=courses)


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
