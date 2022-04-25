import json
from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@localhost:3306/semantic'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.context_processor
def utility_processor():
    def manifest(path):
        f = open('./static/manifest.json')
        path = json.load(f)[path]['file']
        f.close()
        return path
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


@app.route("/", methods=['GET'])
def main():
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
    db.create_all()
    app.debug = True
    app.run()
