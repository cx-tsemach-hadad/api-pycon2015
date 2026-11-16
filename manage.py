#!/usr/bin/env python
import click
from flask.cli import FlaskGroup
from api.app import create_app
from api.models import db, User, Class


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Management commands."""


@cli.command()
@click.option('--testdata', is_flag=True, default=False)
def createdb(testdata):
    """Create the database, optionally with test data."""
    db.drop_all()
    db.create_all()
    if testdata:
        classes = ['Algebra', 'Literature', 'Chemistry', 'Spanish',
                   'Game Development', 'History', 'Music', 'Psychology',
                   'Science', 'Photography', 'Drama', 'Business',
                   'Python Programming']
        for name in classes:
            c = Class(name=name)
            db.session.add(c)

        u = User(username='miguel', password='python')
        db.session.add(u)

        db.session.commit()


@cli.command()
@click.argument('username')
def adduser(username):
    """Register a new user."""
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format(username))


@cli.command()
def test():
    """Run the unit tests."""
    from subprocess import call
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=api', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover'])


if __name__ == '__main__':
    cli()
