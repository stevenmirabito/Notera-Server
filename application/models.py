from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table, DateTime
from datetime import datetime as dt
from sqlalchemy.orm import relationship
from application.database import Base
import hashlib

student_course_table = Table('student_course_rel', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    realname = Column(String(120))
    email = Column(String(120))

    notes = relationship("Note", backref="student")
    courses = relationship(
        "Course",
        secondary=student_course_table,
        back_populates="students")

    def __init__(self, username=None, realname=None, email=None):
        self.username = username.lower()
        self.realname = realname
        self.email = email.lower()

    def __repr__(self):
        return '<Student %r>' % (self.username)

    def gravatar(self):
        if self.email == None:
            email = ""
        else:
            email = self.email.strip().lower()
        h = hashlib.md5()
        h.update(email)
        return "https://www.gravatar.com/avatar/"+h.hexdigest()+"?s=200&d=retro&r=g"

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    coursename = Column(String(120))
    professor = Column(String(120))

    school_id = Column(Integer, ForeignKey('schools.id'))

    notes = relationship("Note", backref="course")
    students = relationship(
        "Student",
        secondary=student_course_table,
        back_populates="courses")

    def __init__(self, coursename=None, professor=None):
        self.coursename = coursename
        self.professor = professor

    def __repr__(self):
        return '<Course %r>' % (self.coursename)

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    body = Column(Text())
    timestamp = Column(DateTime())

    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

    def __init__(self, title=None, body=None, timestamp=None):
        self.title = title
        self.body = body
        if timestamp:
            self.timestamp = dt.strptime(timestamp,"%Y-%m-%d %H:%M:%S.%f") # ISO 8601
        else:
            self.timestamp = dt.now()

    def __repr__(self):
        return '<Note %r>' % (self.title)

class School(Base):
    __tablename__ = 'schools'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))

    courses = relationship("Course", backref="school")

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<School %r>' % (self.name)
