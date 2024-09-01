from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='registrar_log')
def registrar_log(titulo, fecha):
    try:
        with open('log_usuarios.txt', 'a+') as file:
            file.write('{} - Registro: {}\n'.format(fecha, titulo))
        print('Log registrado con éxito')
    except Exception as e:
        print(f'Error al registrar el log: {e}')
        raise e