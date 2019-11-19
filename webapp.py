import flask
from flask import render_template, request
import json
import sys
import datasource

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/', methods = ["GET", "POST"])
def getNutritionInfo():
    if request.method == "POST":
        #fetch form data
        result = request.form
        food = result['food']
        ds = datasource.Nutrek()
        description = "displaying all nutrients in food and their proportions"
        result = ds.getNutrients(food)
        return render_template('nutrekPrototype.html', result)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
