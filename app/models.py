from app import db, login_manager
from sqlalchemy.ext.hybrid import hybrid_property
from . import bcrypt, db


@login_manager.user_loader
def load_user(username):
    return User.query.get(str(username))


class User(db.Model):
    username = db.Column(db.String(64), index=True,
                         unique=True, primary_key=True)
    rules = db.relationship('Rule', backref='author', lazy='dynamic')
    _password = db.Column(db.String(128))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

    def get_id(self):
        return str(self.username)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.username)


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    version = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.username'))

    def __repr__(self):
        return '<Rule %r>' % (self.body)
