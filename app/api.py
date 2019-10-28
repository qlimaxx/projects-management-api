import random

from flask import Blueprint, g, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

from .enums import Role, Status
from .models import Project, Result, Test, User, db
from .utils import is_valid_email, is_valid_hash, require_role, response_error


api = Blueprint('api', __name__)

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.phash, password):
            g.user = user
            return True
    return False


@api.route('/user', methods=['POST'])
@auth.login_required
@require_role(Role.ADMIN)
def create_user():
    email = request.json.get('email', '')
    if not is_valid_email(email):
        return response_error('Email is invalid.', 400)
    if User.query.filter_by(email=email).first():
        return response_error('User is already exists.', 400)
    phash = request.json.get('phash', '')
    if not is_valid_hash(phash):
        return response_error('Password hash is invalid.', 400)
    role = request.json.get('role', '')
    try:
        Role(role)
    except ValueError:
        return response_error('Role is invalid.', 400)
    user = User(email=email, phash=phash, role=role, created_by=g.user.id)
    db.session.add(user)
    db.session.commit()
    return jsonify({'email': user.email,
                    'phash': user.phash,
                    'role': user.role})


@api.route('/project', methods=['POST'])
@auth.login_required
@require_role(Role.MANAGER)
def create_project():
    name = request.json.get('name', '')
    if not name:
        return response_error('Name is invalid.', 400)
    if Project.query.filter_by(name=name).first():
        return response_error('Project is already exists.', 400)
    project = Project(name=name, user=g.user)
    db.session.add(project)
    db.session.commit()
    return jsonify({'name': project.name})


@api.route('/<string:project_name>/test', methods=['POST'])
@auth.login_required
@require_role(Role.QA_MANAGER)
def create_test(project_name):
    name = request.json.get('name', '')
    if not name:
        return response_error('Name is invalid.', 400)
    project = Project.query.filter_by(name=project_name).first()
    if not project:
        return response_error('Project is not found.', 404)
    test = Test(name=name, project=project, user=g.user)
    db.session.add(test)
    db.session.commit()
    return jsonify({'name': test.name})


@api.route('/<string:project_name>/<string:test_name>/run', methods=['POST'])
@auth.login_required
@require_role(Role.USER)
def run_test(project_name, test_name):
    project = Project.query.filter_by(name=project_name).first()
    if not project:
        return response_error('Project is not found.', 404)
    test = Test.query.filter_by(name=test_name, project=project).first()
    if not test:
        return response_error('Test is not found.', 404)
    result = Result(test=test, user=g.user,
                    status=random.choice(list(Status)).value)
    db.session.add(result)
    db.session.commit()
    return jsonify({'id': result.run_id})


@api.route(
    '/<string:project_name>/<string:test_name>/<uuid:run_id>',
    methods=['GET'])
@auth.login_required
@require_role(Role.USER)
def check_result(project_name, test_name, run_id):
    project = Project.query.filter_by(name=project_name).first()
    if not project:
        return response_error('Project is not found.', 404)
    test = Test.query.filter_by(name=test_name, project=project).first()
    if not test:
        return response_error('Test is not found.', 404)
    result = Result.query.filter_by(run_id=run_id, test=test).first()
    if not result:
        return response_error('Test result is not found.', 404)
    return jsonify({'status': result.status})
