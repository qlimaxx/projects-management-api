import click
from werkzeug.security import generate_password_hash

from app import create_app
from app.enums import Role
from app.models import User, db


app = create_app()


@app.cli.command('create-db')
def create_db():
    db.drop_all()
    db.create_all()
    print('Database is created.')


@app.cli.command('create-admin')
@click.argument('email', default='admin@mail.com')
@click.argument('password', default='admin')
def create_admin(email, password):
    try:
        user = User(
            email=email,
            phash=generate_password_hash(password),
            role=Role.ADMIN.value)
        db.session.add(user)
        db.session.commit()
        print('Admin(email={0}, password={1}) is created.'.format(
            email, password))
    except Exception as ex:
        print(ex)


@app.cli.command('generate-password-hash')
@click.argument('password')
def _generate_password_hash(password):
    print(generate_password_hash(password))
