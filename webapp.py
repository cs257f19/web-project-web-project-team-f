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

def getProductName(food):
    allFood = ds.getFoodAvailable(food)
    productName = allFood[0]
    result = ""
    for item in productName:
       result += item + " "
    return result 

'''Translates HTML form data into a database query and then into a results page'''
@app.route("/search", methods = ["POST", "GET"])
def getSearchResults():
    if request.method == "POST":
        foodsearched = request.form["foodsearch"]
        while foodsearched[0] == " ":
            foodsearched = foodsearched.replace(foodsearched[0],"")
        searchresults = ds.getFoodAvailable(foodsearched)
        if  searchresults is None:
            result =  "We do not have any data on " + foodsearched 
            result = {result:0}
            return render_template("searchResults.html", result=result)
        allProducts = {}
        for item,index in enumerate(searchresults):
            finalProduct = ""
            for i in index:
                finalProduct += i + " "
            allProducts[index] = finalProduct
        return render_template("searchResults.html", result=allProducts)

'''Translates HTML form data into a database query and then into a results page'''
@app.route("/results", methods = ["POST", "GET"])
def getResults():
    querySelection = request.form["query"]
    
    if request.method == "POST":
        food = request.form["food"]
        
        while food[0] == " ":
            food = food.replace(food[0],"")
            
        if querySelection == "nutritionfacts":
            currentFood = ds.getFoodAvailable(food)
            result = ds.getNutrients(food)
            finalResult = {}
            
            if result is None:
               result = "This item "+ food + " does not exist in our database."
               result = {result:0}
               return render_template("nutrients.html", result=result)
            
            for key in result:
                finalResult[key] = result[key]
            return render_template("nutrients.html", result=finalResult)
        
        elif querySelection == "ingredients":
            ingredients = ds.getIngredientBreakDown(food)
            
            if ingredients is None:
                result =  "We do not have any data on " + food 
                result = {result:0}
                return render_template("ingredients.html", result=result)
            allIngredients = {}
            allIngredients[getProductName(food)]=0
            for item,index in enumerate(ingredients):
                allIngredients[index] = item
            return render_template("ingredients.html", result=allIngredients)
        
        elif querySelection == "allergy":
            allergen = request.form["allergen"]
            
            if len(allergen) == 0:
                result = {"You did not enter an allergen.":0}
            
            else:
                while allergen[0] == " ":
                    allergen = allergen.replace(allergen[0],"")
            
                result = ds.containsAllergen(food, allergen)
                
                if result is True:
                   result =  "WARNING! " + getProductName(food) + " contains the allergen: " + allergen
                elif result is False:
                    result =  "No known " + allergen + " allergen in " + getProductName(food) + " according to USDA Food database."
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
    app.run(host=host, port=5219, debug=True)
