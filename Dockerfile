FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

COPY app.py .

RUN pip install --no-cache-dir -r requirements.txt

COPY data data

EXPOSE 8000

CMD ["python", "app.py"]
