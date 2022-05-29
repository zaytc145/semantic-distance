import json
from statistics import mode
import time
from rq import Queue
from flask_caching import Cache
from flask import Flask, jsonify, render_template, request
from app.Services.DocumentService import DocumentService
from app.Services.JournalService import JournalService, printLen
from app.models import Document, KeyWord, db
from flask_marshmallow import Marshmallow
from app.Services.OntologyService import OntologyService
from worker import queue

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "SQLALCHEMY_DATABASE_URI": 'mysql://root:12345@localhost:3306/semantic?charset=utf8mb4',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'UPLOAD_FOLDER': "storage"
}

app = Flask(__name__)
app.config.from_mapping(config)
db.init_app(app)
cache = Cache(app)
ma = Marshmallow(app)

class KeyWordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KeyWord


class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document
    keyWords = ma.Nested(KeyWordSchema, many=True)


@app.context_processor
def utility_processor():
    def manifest(path):
        f = open('static/manifest.json')
        data = json.load(f)[path]
        f.close()
        return dict(css_path=data['css'][0], js_path=data['file'])
    return dict(manifest=manifest)


@app.route('/api/queue', methods=['get'])
def test():
    job = queue.enqueue(printLen)
    time.sleep(4)
    print(job.result)
    return 'ok'


@app.route('/api/test', methods=['get'])
def tst():
    # 24, 19
    ds = DocumentService()
    document1 = Document.query.options(
        db.joinedload(Document.keyWords)).get(25)
    onS = OntologyService()

    newKeywors = []
    for concept in [onS.getConcept(word.name) for word in document1.keyWords]:
        if concept:
            children = onS.getAllChildren(concept['class'])
            parent = onS.getAllParent(concept['class'])
            newKeywors = newKeywors + children + parent

    newKeywors = set(newKeywors)
    for word in newKeywors:
        document1.keyWords.append(
            KeyWord(name=word.lower(), fromOntology=True))
    db.session.add(document1)
    db.session.commit()
    return 'ok'


@app.route('/api/docs/<docId>', methods=['get'])
def getDocument(docId):
    document = Document.query.options(
        db.joinedload(Document.keyWords)).get(docId)
    documentSchema = DocumentSchema()
    output = documentSchema.dump(document)
    return jsonify({'doc': output})


@app.route('/api/docs', methods=['get'])
def getDocuments():
    documents = Document.query.options().all()
    if not len(documents):
        libSV = JournalService()
        libSV.parseJournal()
        documents = Document.query.options().all()

    documentsSchema = DocumentSchema(many=True)
    output = documentsSchema.dump(documents)
    return jsonify({'docs': output})


@app.route('/api/concepts/compare', methods=['post'])
def compareConcepts():
    request_data = request.get_json()
    ontologySV = OntologyService()
    label_1 = request_data['label_1']
    label_2 = request_data['label_2']

    concept1 = ontologySV.getConcept(label_1.lower())
    concept2 = ontologySV.getConcept(label_2.lower())
    sim = ontologySV.dijkstra(concept1, concept2)
    return {
        'concept1': concept1,
        'concept2': concept2,
        'sim': sim
    }


@app.route('/', defaults={'u_path': ''})
@app.route("/<path:u_path>", methods=['GET'])
def main(u_path):
    return render_template('index.html')


if __name__ == "__main__":
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    app.run()
