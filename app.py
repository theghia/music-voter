"""
This file starts the application and will hold blueprints of other routes that this web application will access.

The homepage is defined here - home.html
"""
import os
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)