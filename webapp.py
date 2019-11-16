import flask
from flask import render_template
import json
import sys

app = flask.Flask(__name__)

@app.route('/web/')
def nutrek():
    return render_template('nutrek.html')



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
