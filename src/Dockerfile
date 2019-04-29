FROM python:3.6

ENV PYTHONUNBUFFERED = 1
ENV APP_DIR=/flask-app

WORKDIR $APP_DIR/

ADD requirements.txt $APP_DIR

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

ADD . $APP_DIR

CMD python manage.py runserver
