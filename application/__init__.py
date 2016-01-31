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

@app.route("/api/student/<uname>/")
def student_route(uname):
    student = models.Student.query.filter_by(username=uname).first()
    return jsonify(row2dict(student))

@app.route("/api/student/<uname>/courses")
def student_courses_route(uname):
    student = models.Student.query.filter_by(username=uname).first()
    response = []
    for course in student.courses:
        response.append(row2dict(course))
    return jsonify(response)

@app.route("/api/student/<uname>/notes")
def student_notes_route(uname):
    student = models.Student.query.filter_by(username=uname).first()
    response = []
    for note in student.notes:
        response.append(row2dict(note))
    return jsonify(response)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
