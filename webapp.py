import flask
from flask import render_template, request
import json
import sys
import datasource

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

@app.route("/search", methods = ["POST", "GET"])
def getSearchResults():
    '''Translates HTML form data into a database query and then into a results page'''
    if request.method == "POST":
        foodsearched = request.form["foodsearch"]
        if len(foodsearched) == 0:
            result = "No results. You did not enter anything."
            result = {result:result}
            return render_template("searchResults.html", result=result)
        searchresults = ds.getFoodAvailable(foodsearched)
        if  searchresults is None or searchresults == []:
            results =  "No results for \"" + foodsearched + "\". Search new food."
            results = {results:results}
            return render_template("searchResults.html", result=results)
        allProducts = {foodsearched:foodsearched}
        for item,index in enumerate(searchresults):
            finalProduct = " ".join(index)
            productList = finalProduct.split(" ")
            finalProduct = " ".join(productList) 
            allProducts[item] = finalProduct 
        removedDuplicates = {}    
        for key in allProducts:
            if allProducts[key] not in removedDuplicates.values():
                removedDuplicates[key] = allProducts[key] 
        return render_template("searchResults.html", result=removedDuplicates)

def nutritionResults(food):
    '''Gets results of getNutrients and returns output result'''
    result = ds.getNutrients(food)
    finalResult = {}
    if result is None:
        result = food + " does not have any nutritional data in database."
        result = {result:result}
        return result
    else:
        for key in result:
            finalResult[key] = result[key]
        return finalResult

def ingredientResults(food):
    '''Gets results of getIngredientBreakdown and returns output result'''
    ingredients = ds.getIngredientBreakDown(food)
    if ingredients == None:
        result =  "We do not have any data on " + food 
        result = {result:result}
        return result
    else:
        allIngredients = {}
        allIngredients[food]=0
        ingredients = ingredients[0]
        if None in [ingredients]:
            result = food + " does not have any ingredients data in database."
            result = {result:result}
            return result
        else:
            ingredients = ingredients.split(",")
            for item,index in enumerate(ingredients):
                allIngredients[index] = item
            return allIngredients

def allergyResults(food,allergen):
    '''Gets results of containsAllergen and returns output result'''
    result = ds.containsAllergen(food, allergen)
    if result is True:
        result =  "WARNING! " + food + " contains the allergen: " + allergen
        result = {result:result}
        return result
    elif None in [result]:
        result = "We are unable to search for any food allergens in " + food + " since it does not have any ingredients data in the database."
        result = {result:result}
        return result
    else:
        result =  "No known " + allergen + " allergen in " + food + " according to USDA Food database."
        result = {result:result}
        return result

@app.route("/results", methods = ["POST", "GET"])
def getResults():
    '''Translates HTML form data into a database query and then into a results page'''
    querySelection = request.form["query"]
    if request.method == "POST":
        food = request.form["food"]
        if querySelection == "nutritionfacts":
            results1 = nutritionResults(food)
            return render_template("nutrients.html", result=results1)
        elif querySelection == "ingredients":
            results2 =ingredientResults(food)
            return render_template("ingredients.html", result=results2)
        elif querySelection == "allergy":
            allergen = request.form["allergen"]
            results3 = allergyResults(food,allergen)
            return render_template("allergens.html", result=results3)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()
    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port, debug=True)
