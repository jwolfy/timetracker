import time
import json

from dataclasses import dataclass, asdict, fields
from typing import Optional
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean)

    @classmethod
    def get(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()


class Issue(db.Model):
    __tablename__ = 'issue'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    issue_id = db.Column(db.Integer, nullable=False, index=True)
    subject = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    __table_args__ = (db.UniqueConstraint('issue_id', 'user_id'), )

    @classmethod
    def get(cls, current_user, issue_id):
        return cls.query.filter_by(user_id=current_user.id, issue_id=issue_id).first()

    def as_dict(self) -> dict:
        return {
            'issue_id': self.issue_id,
            'subject': self.subject,
            'is_active': self.is_active,
        }


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=True, index=True)
    comment = db.Column(db.String(200), nullable=False)
    spent_on = db.Column(db.Date, nullable=False, index=True)
    duration = db.Column(db.Integer, default=0)

    @classmethod
    def get(cls, current_user, id):
        return cls.query.filter_by(user_id=current_user.id, id=id).first()

    @classmethod
    def date_to_str(cls, date: datetime.date) -> str:
        if date:
            return date.strftime('%Y-%m-%d')
        return None

    @classmethod
    def str_to_date(cls, date_str: str) -> datetime.date:
        if date_str:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        return None

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'issue_id': self.issue_id,
            'comment': self.comment,
            'spent_on': Task.date_to_str(self.spent_on),
            'duration': self.duration,
        }


class Timer(db.Model):
    __tablename__ = 'timer'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, index=True)
    is_running = db.Column(db.Boolean, nullable=False, default=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)
    started_at = db.Column(db.Integer, nullable=True)
    task = db.relationship('Task')

    def as_dict(self) -> dict:
        return {
            'is_running': self.is_running,
            'task_id': self.task_id,
            'started_at': self.started_at,
            'elapsed': int(time.time()) - self.started_at if self.is_running else 0,
            'task': self.task.as_dict() if self.task else None,
        }

    def start(self, task_id) -> dict:
        self.is_running = True
        self.task_id = task_id
        self.started_at = int(time.time())

    def stop(self):
        self.is_running = False
        self.task_id = None
        self.started_at = None


@dataclass
class SettingsData:
    redmine_url: str = ''


def settings_data_from_dict_as_str(data: dict) -> str:
    settings_data = SettingsData()
    for field in fields(settings_data):
        name = field.name
        if name in data:
            setattr(settings_data, name, data[name])
    return json.dumps(asdict(settings_data))


class Settings(db.Model):
    __tablename__ = 'settings'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    data = db.Column(db.String)

    @classmethod
    def get(cls, user_id):
        data = cls.query.filter_by(user_id=user_id).first()
        if not data:
            return cls._create_new_and_return(user_id)
        return data

    @classmethod
    def _create_new_and_return(cls, user_id):
        data = asdict(SettingsData())
        settings = Settings(
            user_id=user_id,
            data=json.dumps(data),
        )
        db.session.add(settings)
        db.session.commit()
        return settings

    def as_dict(self) -> dict:
        return json.loads(self.data)
