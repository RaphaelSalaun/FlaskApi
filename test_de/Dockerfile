FROM python:3.10.2-bullseye

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY ./flask_app/install/requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY ./flask_app/*.py /usr/src/app/