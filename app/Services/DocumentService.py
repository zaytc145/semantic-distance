from importlib.resources import path
from werkzeug.utils import secure_filename
import os
from app.models import Document, db


class DocumentService:

    def __init__(self, path):
        self.path = path

    def saveFile(self, file):
        filename = secure_filename(file.filename)
        path = os.path.join(self.path, filename)
        file.save(path)
        document = Document(name=filename, path=path)
        db.session.add(document)
        db.session.commit()
        return document
