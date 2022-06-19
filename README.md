$ cd myproject

Creation of virtual environment
$ python3 -m venv venv

Virtual environment activation
$ . venv/bin/activate

Install python libs
$ pip install -r /path/to/requirements.txt

Install Node.js libs
$ npm i
$ npm run build

Run docker
$ docker-compose up

Run queue worker
$ celery -A main.celery  worker --loglevel=INFO --pool=eventlet