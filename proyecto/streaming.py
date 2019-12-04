import time
from datetime import datetime
from flask import Flask, Response

app = Flask(__name__)


@app.route('/time')
def doyouhavethetime():
    def generate():
        while True:
            yield "{}\n".format(datetime.now().isoformat())
            time.sleep(1)
    return Response(generate(), mimetype='text/plain')

app.run()