from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
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

users = []

def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None