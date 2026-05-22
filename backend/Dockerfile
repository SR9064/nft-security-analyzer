FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y graphviz

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]
# force rebuild Fri May 22 06:21:43 UTC 2026
