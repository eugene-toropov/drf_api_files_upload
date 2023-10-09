FROM python:3.11.6-alpine

WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt --default-timeout=60
COPY ./app /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]