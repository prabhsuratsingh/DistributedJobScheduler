import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)

QUEUE_NAME = "job_queue"

def enqueue_job(run_id):
    redis_client.lpush(QUEUE_NAME, run_id)

def dequeue_job():
    run_id = redis_client.brpop(QUEUE_NAME)
    return run_id