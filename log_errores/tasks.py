from celery import Celery
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - SERVICE-STATUS - %(message)s')

# Crear un manejador de archivo para almacenar logs
log_filename = datetime.datetime.now().strftime('/logs/service_monitor_%Y%m%d_%H%M%S.log')
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Crear un manejador de consola para mostrar logs en terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

celery_app = Celery(__name__, broker='redis://redis:6379/0')


celery_app.conf.update(
    worker_hijack_root_logger=False
)

# Set Celery's logger to a higher log level to filter out its logs
celery_logger = logging.getLogger('celery')
celery_logger.setLevel(logging.CRITICAL +1)

@celery_app.task(name='notify_service_down')
def notify_service_down(service_name, status_code, failure_time):
    if status_code == 200:
        logger.info(f'{service_name} - OK')
    else:
        logger.error(f'{service_name} - FAIL with status code {status_code}')
