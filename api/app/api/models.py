import time

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

    __table_args__ = (db.UniqueConstraint('issue_id', 'user_id'),)

    @classmethod
    def get(cls, current_user, issue_id):
        return cls.query.filter_by(user_id=current_user.id, issue_id=issue_id).first()


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


class Timer(db.Model):
    __tablename__ = 'timer'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, index=True)
    is_running = db.Column(db.Boolean, nullable=False, default=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)
    started_at = db.Column(db.Integer, nullable=True)

    def as_dict(self) -> dict:
        return {
            'is_running': self.is_running,
            'task_id': self.task_id,
            'started_at': self.started_at,
            'elapsed': int(time.time()) - self.started_at if self.is_running else 0,
        }

    def start(self, task_id) -> dict:
        self.is_running = True
        self.task_id = task_id
        self.started_at = int(time.time())

    def stop(self):
        self.is_running = False
        self.task_id = None
        self.started_at = None
