from flask import Flask, render_template, jsonify, request
from mongodb import get_courses, get_course_by_id, get_expired_courses  # Import functions to get courses from MongoDB

app = Flask(__name__)  # Initialize the Flask application

# Route for the homepage (index page)
@app.route('/')
def home():
    page = request.args.get('page', default=1, type=int)
    per_page = 9
    all_courses, total_courses = get_courses(page, per_page)
    total_pages = (total_courses + per_page - 1) // per_page

    return render_template('courses.html',
                           courses=all_courses,
                           page=page,
                           total_pages=total_pages)


@app.route('/home')
def index_page():
    return render_template('index.html')


@app.route('/courses', methods=['GET'])
def courses():
    page = request.args.get('page', default=1, type=int)
    per_page = 9
    all_courses, total_courses = get_courses(page, per_page)

    total_pages = (total_courses + per_page - 1) // per_page  # ceiling division

    return render_template('courses.html', courses=all_courses,page=page,total_pages=total_pages)
    
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

@app.route('/expired')
def expired_courses():
    page = request.args.get('page', default=1, type=int)
    per_page = 9
    courses, total_courses = get_expired_courses(page, per_page)
    total_pages = (total_courses + per_page - 1) // per_page

    return render_template('expired_courses.html',
                           courses=courses,
                           page=page,
                           total_pages=total_pages)



# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
