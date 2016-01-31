from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from application.database import Base

student_course_table = Table('student_course_rel', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    realname = Column(String(120))

    notes = relationship("Note", backref="student")
    courses = relationship(
        "Course",
        secondary=student_course_table,
        back_populates="students")

    def __init__(self, username=None, realname=None):
        self.username = username.lower()
        self.realname = realname

    def __repr__(self):
        return '<Student %r>' % (self.username)

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    coursename = Column(String(120))
    professor = Column(String(120))

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

    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))

    def __init__(self, title=None, body=None):
        self.title = title
        self.body = body

    def __repr__(self):
        return '<Note %r>' % (self.title)