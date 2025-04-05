from datetime import datetime
from flask import Flask, jsonify, send_file
from prometheus_client import start_http_server, Counter, Histogram, Summary
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import io

app = Flask(__name__)

# Метрики Prometheus:
# количество запросов по всем эндпоинтам
REQUESTS = Counter('app_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
# нагрузка
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency', ['method', 'endpoint'])
# кол-во ошибок
ERRORS = Counter('app_errors_total', 'Total errors', ['method', 'endpoint'])
# суммарное время обработки запросов
REQUEST_TIME_SUMMARY = Summary('app_request_processing_time_seconds', 'Time spent processing requests', ['method', 'endpoint'])

@app.route('/health')
def health():
    REQUESTS.labels(method='GET', endpoint='/health').inc()
    return jsonify(status="OK")

@app.route('/stress')
def stress():
    start = time.time()
    time.sleep(random.uniform(0.1, 1.0))
    latency = time.time() - start
    REQUEST_LATENCY.labels(method='GET', endpoint='/stress').observe(latency)
    REQUEST_TIME_SUMMARY.labels(method='GET', endpoint='/stress').observe(latency)
    return jsonify(status="Stress test completed")

@app.route('/error')
def error():
    REQUESTS.labels(method='GET', endpoint='/error').inc()
    if random.choice([True, False]):
        ERRORS.labels(method='GET', endpoint='/error').inc()
        return jsonify(error="An error occurred!"), 500
    return jsonify(status="No error occurred.")

@app.route('/info')
def info():
    REQUESTS.labels(method='GET', endpoint='/info').inc()
    return jsonify(app_name="My Flask App", version="1.0.0", description="This is a simple Flask application with Prometheus metrics. Practice 206.")

@app.route('/love')
def cat():
    REQUESTS.labels(method='GET', endpoint='/love').inc()

    plt.figure(figsize=(8, 8))
    t = np.linspace(0, 2 * np.pi, 1000)
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

    plt.fill(x, y, color='red')
    plt.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

@app.route('/')
def index():
    current_time = datetime.now().strftime('%H:%M:%S')
    return f'<b>Hello World at {current_time}</b>!'

if __name__ == '__main__':
    start_http_server(8000)  # Экспорт метрик на порт 8000
    app.run(host='0.0.0.0', port=5000)