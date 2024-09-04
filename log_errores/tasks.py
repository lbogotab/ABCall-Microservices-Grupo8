from celery import Celery

celery_app = Celery(__name__, broker='redis://redis:6379/0')

@celery_app.task(name='notify_service_down')
def notify_service_down(service_name, status_code, failure_time):
    print(f'Received message: {failure_time}: Service {service_name} is DOWN with status code {status_code}')