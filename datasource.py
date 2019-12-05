import psycopg2
import getpass
import random 
class Nutrek:
    '''
    Nutrek executes all of the queries on the database
    and formats the data to send back to the front end'''


    def connect(self, user, password):
        '''
        Establishes a connection to the database with the following credentials:
            user - username, which is also the name of the database
            password - the password for this database on perlman
            Note: exits if a connection cannot be established.
        '''
        try:
            self.connection = psycopg2.connect(host="localhost", database=user, user=user, password=password)
        except Exception as e:
            print("Connection error: ", e)
            exit()

    def disconnect(self):
        '''
        Breaks the connection to the database
        '''
        self.connection.close()

    def getNutrients(self, food):
        '''
        returns all nutrients and the amount of each nutrient in a given food
        '''
        if food == "":
            return None 
        food = food.upper()
        nutrientList = ["ash(g)", "biotin(mcg)", "caffeine(mg)", "calcium(mg)", "carbohydrate by difference(g)", "carbohydrate_other(g)", "cholesterol(mg)",
        "chromium(mcg)", "copper(mg)", "fatty acids total monounsaturated(g)", "fatty acids total polyunsaturated (g)", "fatty acids total saturated(g)", "fatty acids total trans(g)",
        "fiber insoluble(g)", "fiber soluble(g)", "fiber total dietary(g)", "folic acid(mcg)", "iodine(mcg)", "iron(mg)", "lactose(g)",
         "magnesium(mg)", "manganese(mg)", "niacin(mg)", "pantothenic acid(mg)", "phosphorus (mg)", "potassium(mg)",
         "protein(g)", "riboflavin(mg)", "selenium(mcg)", "sodium(mg)", "sugars added(g)", "sugars total(g)", "thiamin(mg)", "total lipid fat(g)",
         "total sugar alcohols(g)", "vitamin a IU" , "vitamin b 12(mcg)", "vitamin b-6(mg)", "vitamin c total ascorbic acid(mg)",
         "vitamin d IU", "vitamin e label entry primarily IU", "vitamin K phylloquinone(mcg)", "water(g)",
         "xylitol(g)", "zinc(mg)"]
        try:
            cursor1 = self.connection.cursor()
            cursor1.execute("SELECT Ash_grams, Biotin_mcg, Caffeine_mg, Calcium_Ca_mg, Carbohydrate_by_difference_g, Carbohydrate_other_g, Cholesterol_mg, Chromium_Cr_mcg, Copper_Cu_mg, Fatty_acids_total_monounsaturated_g, Fatty_acids_total_polyunsaturated_g, Fatty_acids_total_saturated_g, Fatty_acids_total_trans_g, Fiber_insoluble_g, Fiber_soluble_g, Fiber_total_dietary_g, Folic_acid_mcg, Iodine_I_mcg, Iron_Fe_mg, Lactose_g, Magnesium_Mg_mg, Manganese_Mn_mg, Niacin_mg, Pantothenic_acid_mg FROM Nutrek WHERE food_name LIKE " + str("'%"+food+"%'") + ";")
            results1 = cursor1.fetchall()
            cursor2 = self.connection.cursor()
            cursor2.execute("SELECT Phosphorus_P_mg, Potassium_K_mg, Protein_g, Riboflavin_mg, Selenium_Se_mcg, Sodium_Na_mg, Sugars_added_g, Sugars_total_g, Thiamin_mg, Total_lipid_fat_g, Total_sugar_alcohols_g, Vitamin_A_IU , Vitamin_B12_mcg, Vitamin_B6_mg, Vitamin_C_total_ascorbic_acid_mg, Vitamin_D_IU, Vitamin_E_label_entry_primarily_IU, Vitamin_K_phylloquinone_mcg, Water_g, Xylitol_g, Zinc_Zn_mg FROM Nutrek WHERE food_name LIKE " + str("'%"+food+"%'") + ";")
            results2 = cursor2.fetchall()
            fullNutrientList = []
            results = []
   
            for i in results1[0]:
                results.append(i)
            for j in results2[0]:
                results.append(j)
            resultsLength = len(results)
            allFood = self.getFoodAvailable(food)
            specificFood = allFood[0]
            if resultsLength == 0 :
                return None 
            nutrientDictionary = {}
            for nutrient, proportion in zip(nutrientList, results):
                nutrientDictionary[nutrient] = proportion
            proportions = list(nutrientDictionary.values())
            proportionsList = []
            for item in proportions:
                proportionsList.append(float(item))
            while resultsLength > 0 and sum(proportionsList) == 0:
                results = []
                rehashed = random.randint(1,resultsLength)
                for i in results1[rehashed]:
                    results.append(i)
                for j in results2[rehashed]:
                    results.append(j)
                specificFood = allFood[rehashed]
                if resultsLength == 0 :
                   return None 
                nutrientDictionary = {}
                for nutrient, proportion in zip(nutrientList, results):
                    nutrientDictionary[nutrient] = proportion
                proportions = list(nutrientDictionary.values())
                proportionsList = []
                for item in proportions:
                    proportionsList.append(float(item))
                if sum(proportionsList) > 0:
                   return specificFood
                resultsLength -=1
            return specificFood

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getIngredientBreakDown(self, food):
        ''' returns all the ingredients in a given food item'''
        if food == "":
            return None 
        food = food.upper()
        try:
            cursor = self.connection.cursor()
            query = ("SELECT ingredients_english FROM Nutrek WHERE  food_name LIKE " + str("'%"+food+"%'") +";")
            cursor.execute(query)
            results = cursor.fetchall()
            results = results[0]
            FullIngredientList = []
            if results is None:
                return "No known ingredients."
            else:
                for item in results:
                    if "(" in item:
                        item = item.replace("(", "")
                    if "," in item:
                        item = item.replace(",", "")
                    if ")" in item:
                        item = item.replace(")","")
                    FullIngredientList.append(item) 
            return FullIngredientList

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getFoodAvailable(self, food):
        '''returns all foods in database containing or like input food name'''
        if food == "":
            return None 
        food = food.upper()
        try:
            cursor = self.connection.cursor()
            query = ("SELECT food_name FROM Nutrek WHERE food_name LIKE " + str("'%"+food+"%'") +";")
            cursor.execute(query)
            results = cursor.fetchall()
            if results is None:
                return None 
            return results

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def containsAllergen(self, food, allergen):
        '''returns True if food contains allergen (could cause allergic reaction) and false if otherwise '''
        if food == "" or allergen == "":
            return None 
        food = food.upper()
        ingredients = self.getIngredientBreakDown(food)
        FullIngredientList = []
        allergen = allergen.upper()
        if ingredients is None:
            return "No known allergens"
        for item in ingredients:
            if "(" in item:
                item = item.replace("(", "")
            if "," in item:
                item = item.replace(",", "")
            if ")" in item:
                item = item.replace(")","")
            FullIngredientList.append(item)
        try:
            for ing in FullIngredientList:
                if allergen in ing:
                    return True
            return False
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None



    def checkNutrientThreshold(self, food, nutrient):
        '''check if the amount of nutrients in a given food to enable them see if
         they are meeting a nutritional goal.'''
        if food == "" or nutrient == "":
            return None 
        food = food.upper()
        nutrient = nutrient.lower()
        try:
            nutrientDictionary = self.getNutrients(food)
            for item in nutrientDictionary:
                if nutrient in item:
                    return item + ' ' + nutrientDictionary[item]
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

def main():
    user = 'odoome'
    password = 'tiger672carpet'
    #password = getpass.getpass()
    # Connect to the database
    N = Nutrek()
    N.connect(user, password)
#     print(N.containsAllergen("granola", "peanuts"))
#     print(N.containsAllergen("milk", "lactose"))
#     print(N.containsAllergen("fried rice", "oil"))
#     Disconnect from database
#     N.disconnect()
main()
