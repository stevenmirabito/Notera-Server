from flask import Flask, request
from json import dumps as jsonify
from datetime import datetime as dt
from application.database import session as db
from application.util import row2dict
import application.models as models

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:red'>Hello There!</h1>"

@app.route("/classmates/<uname>")
def classmate_route(uname):
    try:
        student = models.Student.query.filter_by(username=uname).first()
        response = []
        for course in student.courses:
            for classmate in course.students:
                if classmate == student:
                    continue
                entry = row2dict(classmate)
                entry["class_id"] = course.id
                entry["gravatar"] = classmate.gravatar()
                response.append(entry)
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)


@app.route("/feed/<uname>")
def feed_route(uname):
    try:
        student = models.Student.query.filter_by(username=uname).first()
        response = []
        for course in student.courses:
            for note in course.notes:
                note_dict = row2dict(note)
                author = models.Student.query.filter_by(id=note.student_id).first()
                author_dict = row2dict(author)
                author_dict["gravatar"] = author.gravatar()
                note_dict["author"] = author_dict
                response.append(note_dict)
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

### Student Routes

@app.route("/student/new", methods=['POST'])
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

@app.route("/students")
def students_route():
    response = []
    for student in models.Student.query.all():
        student_dict = row2dict(student)
        student_dict["gravatar"] = student.gravatar()
        response.append(student_dict)
    return jsonify(response)

@app.route("/student/<uname>", methods=['GET','POST'])
def student_route(uname):
    if(request.method == 'POST'):
        try:
            data = request.get_json(force=True)
            student = models.Student.query.filter_by(username=uname).first()
            for k in data:
                if k == "username":
                    student.username = data[k].lower()
                    continue
                student.__setattr__(k, data[k])
            db.add(student)
            db.commit()
            response = row2dict(student)
        except Exception as e:
            response = dict()
            response["msg"] = e.message
    else:
        try:
            student = models.Student.query.filter_by(username=uname).first()
            response = row2dict(student)
            response["gravatar"] = student.gravatar()
        except Exception as e:
            response = dict()
            response["msg"] = e.message
    return jsonify(response)

@app.route("/student/<uname>/courses")
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

@app.route("/student/<uname>/notes")
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

@app.route("/course/new", methods=['POST'])
def new_course_route():
    data = request.get_json(force=True)
    try:
        course = models.Course(data["coursename"], data["professor"])
        school = models.School.query.filter_by(id=data["school_id"]).first()
        school.courses.append(course)
        db.add(course)
        db.add(school)
        db.commit()
        response = row2dict(course)
        response["msg"] = "Success"
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/courses")
def courses_route():
    response = []
    for course in models.Course.query.all():
        response.append(row2dict(course))
    return jsonify(response)

@app.route("/course/<int:cid>", methods=['GET','POST'])
def course_route(cid):
    if(request.method == 'POST'):
        try:
            data = request.get_json(force=True)
            course = models.Course.query.filter_by(id=cid).first()
            for k in data:
                course.__setattr__(k, data[k])
            db.add(course)
            db.commit()
            response = row2dict(course)
        except Exception as e:
            response = dict()
            response["msg"] = e.message
    else:
        try:
            course = models.Course.query.filter_by(id=cid).first()
            response = row2dict(course)
        except Exception as e:
            response = dict()
            response["msg"] = e.message
    return jsonify(response)

@app.route("/course/<int:cid>/notes")
def course_notes_route(cid):
    try:
        course = models.Course.query.filter_by(id=cid).first()
        response = []
        for note in course.notes:
            note_dict = row2dict(note)
            author = models.Student.query.filter_by(id=note.student_id).first()
            author_dict = row2dict(author)
            author_dict["gravatar"] = author.gravatar()
            note_dict["author"] = author_dict
            response.append(note_dict)
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/course/<int:cid>/students")
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

@app.route("/course/<int:cid>/students/add/<uname>")
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

### Note Routes

@app.route("/note/new", methods=['POST'])
def new_note_route():
    data = request.get_json(force=True)
    try:
        if hasattr(data, "timestamp"):
            note = models.Note(data["title"], data["body"], data["timestamp"])
        else:
            note = models.Note(data["title"], data["body"])
        student = models.Student.query.filter_by(id=data["student_id"]).first()
        course = models.Course.query.filter_by(id=data["course_id"]).first()
        student.notes.append(note)
        course.notes.append(note)
        db.add(student)
        db.add(course)
        db.add(note)
        db.commit()
        response = row2dict(note)
        response["msg"] = "Success"
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/notes")
def notes_route():
    response = []
    for note in models.Note.query.all():
        response.append(row2dict(note))
    return jsonify(response)

@app.route("/note/<int:nid>", methods=['GET','POST'])
def note_route(nid):
    if(request.method == 'POST'):
        try:
            data = request.get_json(force=True)
            note = models.Note.query.filter_by(id=nid).first()
            for k in data:
                if k == "timestamp":
                    note.timestamp = dt.strptime(data["timestamp"],"%Y-%m-%d %H:%M:%S.%f") # ISO 8601
                    continue
                note.__setattr__(k, data[k])
            db.add(note)
            db.commit()
            response = row2dict(note)
        except Exception as e:
            response = dict()
            response["msg"] = e.message
    else:
        try:
            note = models.Note.query.filter_by(id=nid).first()
            response = row2dict(note)
        except Exception as e:
            response = dict()
            response["msg"] = e.message
    return jsonify(response)

@app.route("/note/<int:nid>/student")
def note_student_route(nid):
    try:
        student = models.Note.query.filter_by(id=nid).first().student
        response = row2dict(student)
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/note/<int:nid>/course")
def note_course_route(nid):
    try:
        course = models.Note.query.filter_by(id=nid).first().course
        response = row2dict(course)
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

### School Routes

@app.route("/school/new", methods=['POST'])
def new_school_route():
    data = request.get_json(force=True)
    try:
        school = models.School(data["name"])
        db.add(school)
        db.commit()
        response = row2dict(school)
        response["msg"] = "Success"
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/schools")
def schools_route():
    response = []
    for school in models.School.query.all():
        response.append(row2dict(school))
    return jsonify(response)

@app.route("/school/<int:sid>")
def school_route(sid):
    try:
        school = models.School.query.filter_by(id=sid).first()
        response = row2dict(school)
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)

@app.route("/school/<int:sid>/courses")
def school_courses_route(sid):
    try:
        response = []
        for course in models.School.query.filter_by(id=sid).first().courses:
            response.append(row2dict(course))
    except Exception as e:
        response = dict()
        response["msg"] = e.message
    return jsonify(response)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
