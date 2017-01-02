from project import db

from passlib.hash import bcrypt
import random
import string

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(300),nullable=False,unique=True)
    password_hash = db.Column(db.String(300),nullable=False)

    def __init__(self,email,password):
        self.email = email
        self.password_hash = bcrypt.encrypt(password)

    def validate_password(self,password):
        return bcrypt.verify(password,self.password_hash)

    @property
    def serialize(self):
        return {
            'email': self.email
            }
