from redis import Redis
from rq import Connection, Queue, Worker
from app.models import db, SimilarityValue

redis = Redis(password='12345')
queue = Queue('docs', connection=redis)

worker = Worker([queue],connection=redis, name='default')

def printLen(app):
    with app.app_context():
        sim = SimilarityValue(firstDoc=1,secondDoc=2,value=0.15)
        db.session.add(sim)
        db.session.commit()
        return 'hello'

if __name__ == '__main__':
    with Connection(redis):
        worker.work()