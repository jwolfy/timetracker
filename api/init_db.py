from app import create_app
from app.api.models import db


with create_app().app_context() as ctx:
    db.create_all()
