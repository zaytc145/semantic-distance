import json
from statistics import mode
import redis
from rq import Queue
from flask_caching import Cache
from flask import Flask, jsonify, render_template, request
from app.Services.DocumentService import DocumentService
from app.models import Document, db
from flask_marshmallow import Marshmallow

from app.Services.OntologyService import OntologyService

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "SQLALCHEMY_DATABASE_URI": 'mysql://root:12345@localhost:3306/semantic',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'UPLOAD_FOLDER': "./storage"
}

app = Flask(__name__)
app.config.from_mapping(config)
db.init_app(app)
cache = Cache(app)
r = redis.Redis()
q = Queue(connection=r)
ma = Marshmallow(app)

class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document

@app.context_processor
def utility_processor():
    def manifest(path):
        f = open('static/manifest.json')
        data = json.load(f)[path]
        f.close()
        print(data['css'][0])
        return dict(css_path=data['css'][0], js_path=data['file'])
    return dict(manifest=manifest)


@app.route('/api/docs', methods=['get', 'post'])
def fileUpload():
    if request.method == 'GET':
        documents = Document.query.all()
        documentsSchema = DocumentSchema(many=True)
        output = documentsSchema.dump(documents)
        return jsonify({'docs': output})
    if request.method == 'POST':
        docService = DocumentService(app.config['UPLOAD_FOLDER'])
        document = docService.saveFile(request.files['fileuploader'])
        documentSchema = DocumentSchema()
        output = documentSchema.dump(document)
        return dict(document=output)


@app.route('/api/concepts/compare', methods=['post'])
def compareConcepts():
    request_data = request.get_json()
    ontologySV = OntologyService()
    label_1 = request_data['label_1']
    label_2 = request_data['label_2']

    concept1 = ontologySV.getConcept(label_1)
    concept2 = ontologySV.getConcept(label_2)
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
