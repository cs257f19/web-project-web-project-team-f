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
    return render_template("nutrek.html")

'''Translates HTML form data into a database query and then into a results page'''
@app.route("/results", methods = ["POST", "GET"])
def resultNutrients():
    querySelection = request.form["query"]
    if request.method == "POST":
        food = request.form["food"]
        if querySelection is None:
            return "Please select from the options provided."
        if querySelection == "nutritionfacts":
            result = ds.getNutrients(food)
            return render_template("results.html", result = result)
        elif querySelection == "ingredients":
            ingredients = ds.getIngredientBreakDown(food)
            allIngredients = {}
            for item,index in enumerate(ingredients):
                allIngredients[index] = item
            return render_template("results.html", result=allIngredients)
        elif querySelection == "allergy":
            allergen = request.form["allergen"]
            result = ds.containsAllergen(food, allergen)
            if result is True:
                return "WARNING! " + food + " contains the allergen: " + allergen
            else:
                return "No known " + allergen + " allergen in " + food + " according to USDA Food database."


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port, debug=True)
