FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["panel", "serve", "app.py", "--port", "8501", "--address", "0.0.0.0", "--allow-websocket-origin=*"]