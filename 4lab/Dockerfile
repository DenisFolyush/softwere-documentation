FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "-m", "app.main", "--config", "config.json", "--limit", "1000", "--output", "parking_violations_2019.json", "--format", "json", "--summary"]
