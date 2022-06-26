from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(100), nullable=False, default='processing')
    # path = db.Column(db.String(100), nullable=False)
    keyWords = db.relationship('KeyWord', lazy=True)
    similarities = db.relationship(
        'SimilarityValue', lazy=True, foreign_keys="[SimilarityValue.secondDocId]", order_by="desc(SimilarityValue.value)")


class KeyWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    documentId = db.Column(db.Integer, db.ForeignKey('document.id'))
    fromOntology = db.Column(db.Boolean, default=False)

class SimilarityValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstDocId = db.Column(db.Integer, db.ForeignKey('document.id'))
    secondDocId = db.Column(db.Integer, db.ForeignKey('document.id'))
    value = db.Column(db.Numeric(3, 2))

    firstDoc = db.relationship('Document', lazy=True, foreign_keys=[firstDocId])
