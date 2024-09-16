FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY app.py app.py

RUN pip install --no-cache-dir -r requirements.txt

COPY data /data

EXPOSE 8000

CMD ["python", "app.py"]