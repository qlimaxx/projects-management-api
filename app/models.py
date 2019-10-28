from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=True)


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=True)
    user = db.relationship(
        'User', backref=db.backref('projects', lazy=True))


class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'projects.id'), nullable=False)
    project = db.relationship(
        'Project', backref=db.backref('tests', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    user = db.relationship(
        'User', backref=db.backref('tests', lazy=True))


class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(UUID(as_uuid=True), default=uuid4)
    status = db.Column(db.String(100), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey(
        'tests.id'), nullable=False)
    test = db.relationship(
        'Test', backref=db.backref('results', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    user = db.relationship(
        'User', backref=db.backref('results', lazy=True))
