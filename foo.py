from flask import Flask
app = Flask(__name__)

@app.route('/')
def form_log_expense():
    return app.send_static_file('form_log_expense.html')


@app.route('/post-expense', methods=['POST'])
def post_expense():
    return 'posted'