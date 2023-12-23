FROM python:3.10
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt -q
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
