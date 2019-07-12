FROM python:3.7.2

# Set workdir
WORKDIR /usr/app

COPY . .

RUN pip install pipenv
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

EXPOSE 7000

RUN gunicorn --config gunicorn_conf.py wsgi:app