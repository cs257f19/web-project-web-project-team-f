import psycopg2
import getpass
import random
import string

class Nutrek:
    '''
    Nutrek executes all of the queries on the database
    and formats the data to send back to the front end'''
    printable = string.ascii_letters + string.digits + string.punctuation + ' '


    def connect(self, user, password):
        '''
        Establishes a connection to the database with the following credentials (parameters):
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
    
    def cleanNutrients(self, nutrients):
        '''remove special characters from final output '''
        result = ""
        for item in nutrients:
            if "(" in item:
               item = item.replace("(", "")
            if ")" in item:
               item = item.replace(")","")
            result += item + " "
        return result
   
    def cleanIngredients(self,ingredients):
         FullIngredientList = []
         for item in ingredients:
             if "(" in item:
                item = item.replace("(", "")
             if "," in item:
                item = item.replace(",", "")
             if ")" in item:
                item = item.replace(")","")
             if "]" in item:
                item = item.replace("]","")
             if "[" in item:
                item = item.replace("[","")
             if "*" in item:
                item = item.replace("*","")
             if "." in item:
                item = item.replace(".","")
             item = item.upper()
             FullIngredientList.append(item)
         return FullIngredientList
   
        
    def getNutrients(self, food):
        '''
        Returns all nutrients and the amount of each nutrient in a specified food product
        PARAMETERS:
            food - USDA Branded Food Product name of interest
        RETURN:
            a dictionary with pairs of nutrient and amount of that nutrient in the specified food product.
            Note: If sum of nutrient amounts is 0, no nutrition data available for specified food.
        '''
        if food == "":
            return None
        food = food.upper()
        nutrientList = ["Ash (g)", "Biotin (mcg)", "Caffeine (mg)", "Calcium (mg)", "Carbohydrate by difference (g)", "Carbohydrate other (g)", "Cholesterol (mg)",
        "Chromium (mcg)", "Copper (mg)", "Fatty acids total monounsaturated (g)", "Fatty acids total polyunsaturated (g)", "Fatty acids total saturated (g)", "Fatty acids total trans (g)",
        "Fiber insoluble (g)", "Fiber soluble (g)", "Fiber total dietary (g)", "Folic acid (mcg)", "Iodine (mcg)", "Iron (mg)", "Lactose (g)",
         "Magnesium (mg)", "Manganese (mg)", "Niacin (mg)", "Pantothenic acid (mg)", "Phosphorus (mg)", "Potassium (mg)",
         "Protein (g)", "Riboflavin (mg)", "Selenium (mcg)", "Sodium (mg)", "Sugars added (g)", "Sugars total (g)", "Thiamin (mg)", "Total lipid fat (g)",
         "Total sugar alcohols (g)", "Vitamin A IU" , "Vitamin B 12 (mcg)", "Vitamin B 6 (mg)", "Vitamin C total ascorbic acid (mg)",
         "Vitamin D IU", "Vitamin E label entry primarily IU", "Vitamin K phylloquinone (mcg)", "Water (g)",
         "Xylitol (g)", "Zinc (mg)"]
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
            if resultsLength == 0 :
                return None
            nutrientDictionary = {}
            for nutrient, proportion in zip(nutrientList, results):
                nutrientDictionary[nutrient] = proportion
            proportions = list(nutrientDictionary.values())
            proportionsList = []
            for item in proportions:
                proportionsList.append(float(item))
            if sum(proportionsList) == 0:
                return None
            foodName = allFood[0]
            result = self.cleanNutrients(foodName)
            nutrientDictionary[result] =  0 
            return nutrientDictionary

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getIngredientBreakDown(self, food):
        '''
        Returns all the ingredients in a specified food product.
        PARAMETERS:
            food - USDA Branded Food Product name of interest
        RETURN:
            a list of ingredients in the specified food product
            None if no ingredients exist for a given food product or food does not exist.
        '''
        if food == "":
            return None
        food = food.upper()
        try:
            cursor = self.connection.cursor()
            query = ("SELECT ingredients_english FROM Nutrek WHERE  food_name LIKE " + str("'%"+food+"%'") +";")
            cursor.execute(query)
            results = cursor.fetchall()
            if results is None:
                return None
            results = results[0]
            FullIngredientList = []
            if results is None:
                return None
            else:
                for item in results:
                    if "(" in item:
                       item = item.replace("(", "")
                    if ")" in item:
                        item = item.replace(")","")
                    if "]" in item:
                        item = item.replace("]","")
                    if "[" in item:
                        item = item.replace("[","")
                    if "*" in item:
                        item = item.replace("*","")
                    if "." in item:
                        item = item.replace(".","")
                    FullIngredientList.append(item)
            return FullIngredientList

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None
   
    def hex_escape(s):
        return ''.join(c if c in printable else r'\x{0:02x}'.format(ord(c)) for c in s)

    def getFoodAvailable(self, food):
        '''
        Returns all foods in database containing/resembling specified food name.
        PARAMETERS:
            food - USDA Branded Food Product name of interest
        RETURN:
            food products in database containing/resembling specified food name.
            if no food product name resembles input food, returns none.
            '''
        if food == "":
            return None
        food = food.upper()
        print(food)
        try:
            cursor = self.connection.cursor()
            query = ("SELECT food_name FROM Nutrek WHERE food_name LIKE " + str("'%"+food+"%'") +";")
            cursor.execute(query)
            results = cursor.fetchall()
            if results is None:
                return None
            results = sorted(results)
            return results

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def containsAllergen(self, food, allergen):
        '''
        Returns True if food contains allergen and false if otherwise
        PARAMETERS:
            food - USDA Branded Food Product name of interest
            allergen - an ingredient that could cause allergic reaction if an ingredient within food
        RETURN:
            True if specified food contains allergen in its ingredient.
            False if food is missing allergen as ingredient.
            None if food does not exist or no ingredients in database.
        '''
        if food == "" or allergen == "":
            return None
        food = food.upper()
        foodList = self.getFoodAvailable(food)
        if foodList == []:
            return None 
        ingredients = self.getIngredientBreakDown(food)
        allergen = allergen.upper()
        if ingredients == [None]:
            return None 
        
        else:
            FullIngredientList = []
            FullIngredientList = self.cleanIngredients(ingredients)
#             FullIngredientList = []
#             for item in ingredients:
#                 if "(" in item:
#                     item = item.replace("(", "")
#                 if "," in item:
#                     item = item.replace(",", "")
#                 if ")" in item:
#                     item = item.replace(")","")
#                 item = item.upper()
#                 FullIngredientList.append(item)
        try:
            for ingredient in FullIngredientList:
                if allergen in ingredient:
                    return True
            if allergen in FullIngredientList:
                return True
            return False
        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

def main():
    user = "odoome"
    password = "tiger672carpet"
    # Connect to the database
    N = Nutrek()
    N.connect(user, password)
#     print(N.containsAllergen("10 OZ UNIFORM SALMON PORT", "salmon")
#     print(N.containsAllergen("granola", "peanut"))
#     print(N.getFoodAvailable("granola"))
#     print(N.getIngredientBreakDown("granola"))
#     print(N.containsAllergen("",""))
#     print(N.containsAllergen("fried rice", "oil"))
#     Disconnect from database
#     N.disconnect()
main()
