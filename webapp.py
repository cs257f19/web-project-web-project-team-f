import flask
from flask import render_template, request
import json
import sys
import datasource
# Command Line: python3 webapp.py perlman.mathcs.carleton.edu 5219

# Connect to database
ds = datasource.Nutrek()
user = "odoome"
password = "tiger672carpet"
ds.connect(user, password)

app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.route("/", methods = ["POST", "GET"])
def home():
    return render_template("nutrekPrototype.html")

'''Translating HTML form data into a database query and then into a results page'''
@app.route("/results", methods = ["POST", "GET"])
def resultNutrients():
    if request.method == "POST":
        result = request.form["Food"]
        foodName = ds.getFoodAvailable(result)
        description = "Nutrient breakdown"
        result = ds.getNutrients(result)
        return render_template("results.html", result = result, description = foodName)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port, debug=True)
