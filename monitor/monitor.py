import requests
import logging
import time
import datetime
from concurrent.futures import ThreadPoolExecutor
from celery import Celery

celery_app = Celery(__name__, broker='redis://redis:6379/0')


@celery_app.task(name='notify_service_down')
def notify_service_down(*args):
    pass

status_log_queue = 'status_log'

# Endpoints a monitorear
endpoints = {
    'consulta-factura': 'http://nginx/facturacion/consulta-factura/health',
    'download-file': 'http://nginx/facturacion/download-file/health',
    'log-factura': 'http://nginx/facturacion/log-factura/health',
    'realizar-factura': 'http://nginx/facturacion/realizar-factura/health',
}


def check_service(name, url):
    try:
        response = requests.get(url)
        failure_time = datetime.datetime.now().isoformat()
        args = (name, response.status_code, failure_time)
        notify_service_down.apply_async(args=args, queue=status_log_queue)
    except requests.exceptions.RequestException as e:
        args = (name, str(e), failure_time)
        notify_service_down.apply_async(args=args, queue=status_log_queue)


# servicio de monitoreo que utiliza varios hilos para monitorear cada endpoint
def monitor_services():
    with ThreadPoolExecutor(max_workers=len(endpoints)) as executor:
        while True:
            futures = [
                executor.submit(check_service, name, url)
                for name, url in endpoints.items()
            ]
            for future in futures:
                future.result()
            time.sleep(5)  # Tiempo de espera antes de la siguiente verificación


if __name__ == "__main__":
    monitor_services()
