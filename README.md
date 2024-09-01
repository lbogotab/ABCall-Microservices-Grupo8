# Proyecto de Microservicios ABCall - Grupo 8

Este proyecto contiene dos microservicios y utiliza Nginx como API Gateway para redirigir las solicitudes a los microservicios correspondientes.

## Requisitos Previos

- Python 3.x
- Pip
- Virtualenv
- Nginx

## Configuración del Ambiente

### Paso 1: Clonar el Repositorio

Clona este repositorio en tu máquina local:

```sh
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

### Paso 2: Crear y Activar un Entorno Virtual

Crea un entorno virtual y actívalo:

```sh
python -m venv venv
venv\Scripts\activate
```
### Paso 3: Instalar los Requisitos

```sh
pip install -r requirements.txt
```

## Configuración y Ejecución de los Microservicios

Microservicio 1: Usuarios

### 1: Navega al directorio del microservicio de usuarios (ABCall):

```sh
cd microservicio_usuarios
```

### 2: Inicia el microservicio en el puerto 5000:

```sh
flask run --port=5000
```
Microservicio 2: Realizar Factura

### 1: Navega al directorio del microservicio de realizar factura:

```sh
cd microservicio_realizar_factura
```

### 2: Inicia el microservicio en el puerto 5000:

```sh
flask run --port=5001
```
### Configuración de Nginx

### 1: Descargar e Instalar Nginx

### 2: Configurar Nginx

Navega a la carpeta C:\nginx\conf y abre el archivo nginx.conf en un editor de texto.
Agrega la siguiente configuración para redirigir las solicitudes a los microservicios:

```sh
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;

    sendfile        on;
    keepalive_timeout  65;

    server {
        listen       80;
        server_name  localhost;

        location /usuario/ {
            proxy_pass http://127.0.0.1:5000/usuario/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /realizar_factura/ {
            proxy_pass http://127.0.0.1:5001/realizar_factura/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```

### 3: Iniciar Nginx

Abre una terminal de comandos (CMD) como administrador.

Navega a la carpeta donde extrajiste Nginx, por ejemplo, C:\nginx.

Ejecuta el siguiente comando para iniciar Nginx:

```sh
start nginx
```