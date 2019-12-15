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
@app.route("/search", methods = ["POST", "GET"])
def getSearchResults():
    if request.method == "POST":
        foodsearched = request.form["foodsearch"]
        if foodsearched is None:
            result = "No food " + foodsearched 
            result = {result:result}
            return render_template("searchResults.html", result=result)
        if len(foodsearched) == 0:
            result = "You entered nothing."
        searchresults = ds.getFoodAvailable(foodsearched)
        if  searchresults is None:
            result =  "No food containing " + foodsearched + " was found."
            results = {foodsearched:foodsearched}
            results[result]=result
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

'''Translates HTML form data into a database query and then into a results page'''
@app.route("/results", methods = ["POST", "GET"])
def getResults():
    querySelection = request.form["query"]
    
    if request.method == "POST":
        food = request.form["food"]
        if querySelection == "nutritionfacts":
            result = ds.getNutrients(food)
            finalResult = {}
            if result is None:
               result = food + " does not have any nutritional data in database."
               result = {result:result}
               return render_template("nutrients.html", result=result)
            
            for key in result:
                finalResult[key] = result[key]
            return render_template("nutrients.html", result=finalResult)
        
        if querySelection == "ingredients":
            ingredients = ds.getIngredientBreakDown(food)
            
            if ingredients == None:
                print(ingredients, "Aishee, right here.")
                result =  "We do not have any data on " + food 
                result = {result:result}
                return render_template("ingredients.html", result=result)
            else:
                allIngredients = {}
                allIngredients[food]=0
                ingredients = ingredients[0]
                if None in [ingredients]:
                    result = "Hello Mama.Can you fix this sentence? Kind, regards."
                    result = {result:result}
                    return render_template("ingredients.html", result=result)
                ingredients = ingredients.split(",")
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
                   result =  "WARNING! " + food + " contains the allergen: " + allergen
                else:
                    result =  "No known " + allergen + " allergen in " + food + " according to USDA Food database."
                result = {result:result}
            return render_template("allergens.html", result=result)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=5219, debug=True)
#             if len(ingredients) == 1:
#                 allIngredients[ingredients] = 1
#                 return render_template("ingredients.html", result=allIngredients)
