import requests
import logging
import time
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Crear un manejador de archivo para almacenar logs
file_handler = logging.FileHandler('service_monitor.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Crear un manejador de consola para mostrar logs en terminal
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Endpoints a monitorear
endpoints = {
    'consulta-factura': 'http://nginx/facturacion/consulta-factura/health',
    'download-file': 'http://nginx/facturacion/download-file/health',
}


def check_service(name, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info(f'{name} is UP')
        else:
            logger.error(f'{name} is DOWN with status code {response.status_code}')
    except requests.exceptions.RequestException as e:
        logger.error(f'{name} is DOWN with error: {e}')


# servicio de monitoreo que utiliza varios hilos para monitorear cada endpoint
def monitor_services():
    with ThreadPoolExecutor(max_workers=len(endpoints)) as executor:
        while True:
            futures = [executor.submit(check_service, name, url) for name, url in endpoints.items()]
            for future in futures:
                future.result()  
            time.sleep(8)  # Tiempo de espera antes de la siguiente verificación


if __name__ == "__main__":
    monitor_services()
