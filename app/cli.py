import json
import os
from flask import Blueprint
import click

from app.models import User
from app import db

bp = Blueprint("cli", __name__, cli_group=None)


@bp.cli.group()
def translate():
    """Translation and localization commands."""
    pass


@translate.command()
@click.argument("lang")
def init(lang):
    """Initialize a new language."""
    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if os.system("pybabel init -i messages.pot -d app/translations -l " + lang):
        raise RuntimeError("init command failed")
    os.remove("messages.pot")


@translate.command()
def update():
    """Update all languages."""
    if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if os.system("pybabel update -i messages.pot -d app/translations"):
        raise RuntimeError("update command failed")
    os.remove("messages.pot")


@translate.command()
def compile():
    """Compile all languages."""
    if os.system("pybabel compile -d app/translations"):
        raise RuntimeError("compile command failed")


@bp.cli.command('seed-personas')
def seed_personas():
    with open('personas.json', 'r') as f:
        data = json.load(f)
    for member in data['council members']:
        email = member['name'].replace(' ', '.').replace("'", '.') + '@the-council.gov'
        user = User(
            username=member['name'],
            email=email,
            npc=True,
            about_me=str(member)
        )
        db.session.add(user)
    db.session.commit()