FROM python:3.12-slim

RUN python -m pip install fastapi uvicorn numpy pandas scikit-learn

WORKDIR /app

ADD main.py main.py
ADD schemas.py schemas.py
ADD heart_cleveland_upload.csv heart_cleveland_upload.csv

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]