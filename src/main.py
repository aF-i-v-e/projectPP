from flask import Flask, send_file
from datetime import datetime
from flask_cors import CORS
import numpy as np
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    current_time = datetime.now().strftime('%H:%M:%S')
    return f'<b>Hello World at {current_time}</b>!'

@app.route('/plot')
def plot():
    # Генерация данных для графика в форме сердечка
    t = np.linspace(0, 2 * np.pi, 1000)
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

    # Создание графика
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, color='red')
    plt.title('График в форме сердечка')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('equal')  # Устанавливаем равные масштабы по осям
    plt.grid(True)

    # Сохранение графика в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()  # Закрываем график, чтобы освободить память

    # Возвращаем изображение
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
