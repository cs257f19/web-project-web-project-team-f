import flask
from flask import render_template, request
import json
import sys
import datasource

ds = datasource.Nutrek()
user = 'odoome'
password = 'tiger672carpet'
ds.connect(user, password)
app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.route('/', methods = ["GET", "POST"])
def home():
    return render_template('nutrekPrototype.html')

@app.route('/results', methods = ["GET", "POST"])
def getResults():
    resList = ds.getIngredientBreakDown('granola')
    res = ''
    for item in resList:
        res += item + '\n'
    return res  
#     if request.method == "POST":
#         result = request.form
#         food = result['food']
#         ds = datasource.Nutrek()
#         description = "displaying all nutrients in food and their proportions"
# #         result = ds.getNutrients(food)
# #         return render_template('results.html')
#         return description  


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port, debug=True)
