from bucket import bucket
from celery import shared_task

# TODO: can be async?
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 7, 'countdown': 2})
def delete_object_task(self, key):
    result = bucket.delete_object(key=key)
    if not result:
        raise Exception()

@shared_task()
def download_object_task(key):
    bucket.download_object(key)
