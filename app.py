from flask import Flask, request, abort, url_for, redirect
from src.LogService import LogService

app = Flask(__name__)

@app.route('/')
def form_log_expense():
    return app.send_static_file('form_log_expense.html')

@app.route('/post-expense', methods=['POST'])
def post_expense():
    try:
        amount = float(request.form['amount'])
        description = str(request.form['description'])
    except ValueError:
        abort(400)

    log_servie = LogService()

    log_servie.log(amount, description)

    return redirect(url_for('form_log_expense'))