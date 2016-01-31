from flask import Flask, request
import json
from json import dumps as jsonify
from application.database import session as db
from application.util import row2dict
import application.models as models

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:red'>Hello There!</h1>"

@app.route("/api/feed/<uname>")
def feed_route(uname):
    return jsonify({"msg":"Not Implemented","username":uname})

### Student Routes

@app.route("/api/student/new", methods=['POST'])
def new_student_route():
    data = request.get_json(force=True)
    try:
        student = models.Student(data["username"], data["realname"])
        db.add(student)
        db.commit()
        response = row2dict(student)
        response["msg"] = "Success"
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/api/student/<uname>/")
def student_route(uname):
    try:
        student = models.Student.query.filter_by(username=uname).first()
        response = row2dict(student)
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/api/student/<uname>/courses")
def student_courses_route(uname):
    try:
        student = models.Student.query.filter_by(username=uname).first()
        response = []
        for course in student.courses:
            response.append(row2dict(course))
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/api/student/<uname>/notes")
def student_notes_route(uname):
    try:
        student = models.Student.query.filter_by(username=uname).first()
        response = []
        for note in student.notes:
            response.append(row2dict(note))
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

### Course routes

@app.route("/api/course/new", methods=['POST'])
def new_course_route():
    data = request.get_json(force=True)
    try:
        course = models.Course(data["coursename"], data["professor"])
        db.add(course)
        db.commit()
        response = row2dict(course)
        response["msg"] = "Success"
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/api/course/<int:cid>/")
def course_route(cid):
    try:
        course = models.Course.query.filter_by(id=cid).first()
        response = row2dict(course)
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/api/course/<int:cid>/notes")
def course_notes_route(cid):
    try:
        course = models.Course.query.filter_by(id=cid).first()
        response = []
        for note in course.notes:
            response.append(row2dict(note))
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/api/course/<int:cid>/students")
def course_students_route(cid):
    try:
        course = models.Course.query.filter_by(id=cid).first()
        response = []
        for student in course.students:
            response.append(row2dict(student))
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/api/course/<int:cid>/students/add/<uname>")
def course_addstudent_route(cid, uname):
    try:
        course = models.Course.query.filter_by(id=cid).first()
        student = models.Student.query.filter_by(username=uname).first()
        course.students.append(student)
        db.add(student)
        db.add(course)
        db.commit()
        response = dict()
        response["msg"] = "Success"
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
