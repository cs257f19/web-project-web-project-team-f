import flask
from flask import render_template, request
import json
import sys
import datasource
# Command Line: python3 webapp.py perlman.mathcs.carleton.edu 5219

'''Connect to database'''
ds = datasource.Nutrek()
user = "odoome"
password = "tiger672carpet"
ds.connect(user, password)

app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.route("/", methods = ["POST", "GET"])
def home():
    return render_template("nutrek.html")

@app.route("/data", methods = ["POST", "GET"])
def aboutData():
    return render_template("Data.html")

'''Translates HTML form data into a database query and then into a results page'''
@app.route("/results", methods = ["POST", "GET"])
def resultNutrients():
    querySelection = request.form["query"]
    if request.method == "POST":
        food = request.form["food"]
        while food[0] == " ":
            food = food.replace(food[0],"")
        if querySelection == "nutritionfacts":
            currentFood = ds.getFoodAvailable(food)
            result = ds.getNutrients(food)
            finalResult = {}
            finalResult["food name"] = food
            for key in result:
                finalResult[key] = result[key]
            if result is None:
                result = "This item "+ food + " does not exist in our database."
                result = {result:0}
                return render_template("nutrients.html", result=result)
            return render_template("nutrients.html", result=finalResult)
        elif querySelection == "ingredients":
            ingredients = ds.getIngredientBreakDown(food)
            if ingredients is None:
                result =  "We do not have any data on " + food 
                result = {result:0}
                return render_template("ingredients.html", result=result)
            allIngredients = {}
            for item,index in enumerate(ingredients):
                allIngredients[index] = item
            return render_template("ingredients.html", result=allIngredients)
        elif querySelection == "allergy":
            allergen = request.form["allergen"]
            if len(allergen) == 0:
                result = {"You entered nothing.":0}
            else:
                while allergen[0] == " ":
                    allergen = allergen.replace(allergen[0],"")
            
                result = ds.containsAllergen(food, allergen)
                if result is True:
                   result =  "WARNING! " + food + " contains the allergen: " + allergen
                else:
                    result =  "No known " + allergen + " allergen in " + food + " according to USDA Food database."
                result = {result:0}
            return render_template("allergens.html", result=result)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port, debug=True)
