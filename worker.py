from redis import Redis
from rq import Connection, Queue, Worker

redis = Redis(password='12345')
queue = Queue('docs', connection=redis)

worker = Worker([queue],connection=redis, name='default')

if __name__ == '__main__':
    with Connection(redis):
        worker.work()