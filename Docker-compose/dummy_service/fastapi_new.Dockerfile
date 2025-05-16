FROM python:3.10

RUN python -m pip install fastapi==0.103.2 uvicorn

WORKDIR /app

COPY model.py model.py
COPY dummy_fast_api.py dummy_fast_api.py

EXPOSE 5002

CMD ["uvicorn", "dummy_fast_api:app", "--host", "0.0.0.0", "--port", "5002", "--reload"]