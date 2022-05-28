from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(100), nullable=False, default='processing')
    # path = db.Column(db.String(100), nullable=False)
    keyWords = db.relationship('KeyWord',lazy=True)

class KeyWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    documentId = db.Column(db.Integer, db.ForeignKey('document.id'))
    fromOntology = db.Column(db.Boolean, default=False)

# class DocumentKeyWord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     keyWordId = db.Column(db.Integer)
#     documentId = db.Column(db.Integer)

class SimilarityValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstDoc = db.Column(db.Integer)
    secondDoc = db.Column(db.Integer)
    value = db.Column(db.Numeric)
