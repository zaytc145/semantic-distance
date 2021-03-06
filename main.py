import json
from unicodedata import name
from flask import Flask, jsonify, render_template, request
from app.Services.DocumentService import DocumentService
from app.Services.JournalService import JournalService
from app.models import Document, KeyWord, SimilarityValue, db
from flask_marshmallow import Marshmallow
from app.Services.OntologyService import OntologyService
from celery_queue import make_celery

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "SQLALCHEMY_DATABASE_URI": 'mysql://root:12345@localhost:3306/semantic?charset=utf8mb4',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'UPLOAD_FOLDER': "storage",
    'CELERY_CONFIG': {
        'broker_url': 'redis://:12345@localhost:6379',
        'result_backend': 'redis://:12345@localhost:6379',
    }
}

app = Flask(__name__)
app.config.from_mapping(config)
db.init_app(app)
ma = Marshmallow(app)
celery = make_celery(app)


@celery.task(name='task.handle_doc')
def handleDoc(docID):
    docSV = DocumentService()
    print(docID)
    docSV.handleDoc(docID)


class KeyWordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KeyWord


class SimpleDocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document


class SimilaritySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SimilarityValue
    firstDoc = ma.Nested(SimpleDocumentSchema)


class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document
    keyWords = ma.Nested(KeyWordSchema, many=True)
    similarities = ma.Nested(SimilaritySchema, many=True)


@app.context_processor
def utility_processor():
    def manifest(path):
        f = open('static/manifest.json')
        data = json.load(f)[path]
        f.close()
        return dict(css_path=data['css'][0], js_path=data['file'])
    return dict(manifest=manifest)


@app.route('/api/vectors', methods=['get'])
def vectors():
    documents = Document.query.options().all()
    ds = DocumentService()
    for document in documents:
        for doc in documents:
            if doc.id != document.id:
                sim = ds.cosSim(doc, document)
                if sim > 0:
                    simVal = SimilarityValue(
                        firstDocId=doc.id, secondDocId=document.id, value=sim)
                    db.session.add(simVal)
        document.status = 'complete'
        db.session.add(document)
        db.session.commit()
    return 'ok'


@app.route('/api/comparison', methods=['get'])
def comparison():
    ds = DocumentService()
    documentsSchema = DocumentSchema()

    document = Document.query.options(
        db.joinedload(Document.keyWords)
    ).get(6)
    documents = Document.query.options(db.joinedload(Document.keyWords)).all()

    withConceptsNum = 0
    withConcepts = []
    
    for doc in documents:
        if doc.id != document.id:
            sim = ds.cosSim(doc, document)
            if sim > 0:
                withConceptsNum += 1
                withConcepts.append({
                    'doc':  documentsSchema.dump(doc),
                    'value': sim
                })

    noConcepts = []
    noConceptsNum = 0
    document.keyWords = [word for word in document.keyWords if word.fromOntology != 1]
    
    for doc in documents:
        if doc.id != document.id:
            doc.keyWords = [word for word in doc.keyWords if word.fromOntology != 1]
            sim = ds.cosSim(doc, document)
            if sim > 0:
                noConceptsNum += 1
                noConcepts.append({
                    'doc':  documentsSchema.dump(doc),
                    'value': sim
                })
                
    return jsonify({
        'noConcepts': noConcepts,
        'withConcepts': withConcepts,
        'noConceptsNum': noConceptsNum,
        'withConceptsNum': withConceptsNum
    })


@app.route('/api/docs/<docId>', methods=['get'])
def getDocument(docId):
    document = Document.query.options(
        db.joinedload(Document.keyWords)).get(docId)
    documentSchema = DocumentSchema()
    output = documentSchema.dump(document)
    return jsonify({'doc': output})


@app.route('/api/docs', methods=['POST', 'GET'])
def getDocuments():
    if request.method == 'GET':
        documents = Document.query.options().all()
        if not len(documents):
            libSV = JournalService()
            libSV.parseJournal()
            documents = Document.query.options().all()

        documentsSchema = DocumentSchema(many=True)
        output = documentsSchema.dump(documents)
        return jsonify({'docs': output})
    if request.method == 'POST':
        request_data = request.get_json()
        document = Document(name=request_data['name'])
        keywords = [KeyWord(name=keyword)
                    for keyword in request_data['keywords']]
        document.keyWords = keywords
        db.session.add(document)
        db.session.commit()

        handleDoc.delay(document.id)

        documentsSchema = DocumentSchema()
        output = documentsSchema.dump(document)
        return jsonify({'doc': output})


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
