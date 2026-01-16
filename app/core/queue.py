import redis

def get_redis():
    return redis.Redis(
        host="redis",
        port=6379,
        db=0,
        decode_responses=True,
    )


QUEUE_NAME = "job_queue"

def enqueue_job(run_id):
    redis_client = get_redis()

    print(f"From redis enqueue : {run_id}")
    res = redis_client.lpush(QUEUE_NAME, str(run_id))
    print(f"Enqueued: {res}", flush=True)

def dequeue_job():
    redis_client = get_redis()

    print(f"From redis dequeue start")
    queue, run_id = redis_client.brpop(QUEUE_NAME)
    print(f"From redis dequeue : {run_id}")
    return run_id


