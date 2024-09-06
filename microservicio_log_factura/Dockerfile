FROM python:3.12
WORKDIR /flaskr
COPY flaskr /flaskr
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5002
EXPOSE 5002
CMD ["flask", "run"]