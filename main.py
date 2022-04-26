from email.policy import default
import json
import redis
from rq import Queue
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request

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
db = SQLAlchemy(app)
cache = Cache(app)
r = redis.Redis()
q = Queue(connection=r)

@app.context_processor
def utility_processor():
    def manifest(path):
        f = open('static/manifest.json')
        data = json.load(f)[path]
        f.close()
        print(data['css'][0])
        return dict(css_path=data['css'][0], js_path=data['file'])
    return dict(manifest=manifest)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'


@app.route('/api/docs', methods=['post', 'delete'])
def hello():
    return 'hello'


@app.route('/', defaults={'u_path': ''})
@app.route("/<path:u_path>", methods=['GET'])
def main(u_path):
    # student_john = Student(firstname='john',
    #                        lastname='doe',
    #                        email='jd@example.com',
    #                        age=23,
    #                        bio='Biology student')

    # db.session.add(student_john)
    # db.session.commit()

    return render_template('index.html')


if __name__ == "__main__":
    # db.drop_all()
    # db.create_all()
    app.run()
