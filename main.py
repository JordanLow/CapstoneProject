from flask import *

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

app.run('0.0.0.0')