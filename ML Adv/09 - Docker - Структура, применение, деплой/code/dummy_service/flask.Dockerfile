FROM python:3.7

RUN python -m pip install flask gunicorn

WORKDIR /app

ADD model.py model.py
ADD dummy_flask.py dummy_flask.py

EXPOSE 5001

CMD [ "gunicorn", "--bind", "0.0.0.0:5001", "dummy_flask:app" ]