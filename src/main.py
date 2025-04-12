from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"]
)

logging.basicConfig(level=logging.DEBUG)
handler = RotatingFileHandler('main.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

class InputForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    submit = SubmitField('Отправить')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm()
    if form.validate_on_submit():
        name = form.name.data
        current_time = datetime.now().strftime('%H:%M:%S')
        message = f'Привет, {name}! Текущее время: {current_time}.'
        flash(message)
        app.logger.info('Got request')
        app.logger.debug(f'Send message: {message}')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.errorhandler(429)
def ratelimit_error(e):
    app.logger.debug("The limit on requests per minute has been reached")
    return jsonify(error="ratelimit exceeded", message=str(e.description)), 429

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.logger.info(f'Start application on host: {host} port: {port}')
    app.run(debug=False, host=host, port=port)