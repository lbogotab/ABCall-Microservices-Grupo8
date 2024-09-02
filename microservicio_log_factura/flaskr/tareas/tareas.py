from celery import Celery
import json
from datetime import datetime

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task(name='factura_log')
def registrar_log(id_factura, fecha_factura):
    log_path = 'log_facturas.txt'  # Considera usar una ruta absoluta aquí
    print(f'Procesando log para factura ID: {id_factura} con fecha: {fecha_factura}')
    try:
        with open(log_path, 'a+') as file:
            file.write('{} - Registro: {}\n'.format(fecha_factura, id_factura))
        print('Log registrado con éxito')
    except Exception as e:
        print(f'Error al registrar el log: {e}')
        raise e

