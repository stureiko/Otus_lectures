FROM python:3.7

RUN python -m pip install fastapi uvicorn

WORKDIR /app

ADD model.py model.py
ADD dummy_flask.py dummy_flask.py
ADD dummy_fast_api.py dummy_fast_api.py

EXPOSE 5002

CMD ["uvicorn", "dummy_fast_api:app", "--host", "0.0.0.0", "--port", "5002", "--reload"]