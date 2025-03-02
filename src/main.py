from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    current_time = datetime.now().strftime('%H:%M:%S')
    return f'<b>Hello World at {current_time}</b>!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
