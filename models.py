from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from run import db

class User(db.Model, UserMixin):

    __tablename__= 'blog_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256),unique=True, nullable=False)
    password = db.Column(db.String(128),nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.admin = False
        self.authenticated = True
        self.active = True
        self.anonymous = False
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password,password)

    def __repr__(self):
        return f'<User {self.email}>'
    
    def get_id(self):
        return str(self.id)
    
    def is_active(self):
        """True, as all users are active."""
        return True

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()