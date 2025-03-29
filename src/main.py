from flask import Flask
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    current_time = datetime.now().strftime('%H:%M:%S')
    return f'<b>Hello World at {current_time}</b>!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
