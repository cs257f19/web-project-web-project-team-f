import psycopg2
import getpass

class Nutrek:
    '''
    Nutrek executes all of the queries on the database
    and formats the data to send back to the front end'''

    # ***QUESTION 1: UNABLE TO GET INTO DATABASE (USED SLACK PASSWORD)


    def __init__(self):
        self.user = 'mukherjia'
        self.password = 'barn689mango'

    def connect(self):
        '''
        Establishes a connection to the database with the following credentials:
            user - username, which is also the name of the database
            password - the password for this database on perlman
            Note: exits if a connection cannot be established.
        '''
        try:
            connection = psycopg2.connect(database=self.user, user=self.user, password= self.password)
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection

    def disconnect(self, connection):
        '''
        Breaks the connection to the database
        '''
        connection.close()

    def getNutrients(self, connection, food):
        '''
        returns all nutrients and the amount of each nutrient in a given food
        '''
        # ***QUESTION 2 - Syntax okay? i.e. <> operator, we don't need dictionary anymore? We were initially thinking of
        # doing nutrient, nutrient amount (key, value pair in dict, and if all values added was 0, there was insufficient information in database
        # on the nutritional breakdown of food). How can we deal with this issue?
        food = food.upper()
        try:
            cursor = connection.cursor()
            query = "SELECT Ash_grams, Biotin_mcg, Caffeine_mg, Calcium_Ca_mg, Carbohydrate_by_difference_g, Carbohydrate_other_g, Cholesterol_mg, Chromium_Cr_mcg, Copper_Cu_mg, Fatty_acids_total_monounsaturated_g, Fatty_acids_total_polyunsaturated_g, Fatty_acids_total_saturated_g, Fatty_acids_total_trans_g, Fiber_insoluble_g, Fiber_soluble_g, Fiber_total_dietary_g, Folic_acid_mcg, Iodine_I_mcg, Iron_Fe_mg, Lactose_g, Magnesium_Mg_mg, Manganese_Mn_mg, Niacin_mg, Pantothenic_acid_mg, Phosphorus_P_mg, Potassium_K_mg, Protein_g, Riboflavin_mg, Selenium_Se_mcg, Sodium_Na_mg, Sugars_added_g, Sugars_total_g, Thiamin_mg, Total_lipid_fat_g, Total_sugar_alcohols_g, Vitamin_A_IU, Vitamin_B12_mcg, Vitamin_B6_mg, Vitamin_C_total_ascorbic_acid_mg, Vitamin_D_IU, Vitamin_E_label_entry_primarily_IU, Vitamin_K_phylloquinone_mcg, Water_g, Xylitol_g, Zinc_Zn_mg" + "FROM Nutrek" + "WHERE (long_name =" + str(food) + ") AND (Ash_grams <> 0 OR Biotin_mcg <> 0 OR Caffeine_mg <> 0 OR Calcium_Ca_mg <> 0 OR Carbohydrate_by_difference_g <> 0 OR Carbohydrate_other_g <> 0 OR Cholesterol_mg <> 0 OR Chromium_Cr_mcg <> 0 OR Copper_Cu_mg <> 0 OR Fatty_acids_total_monounsaturated_g <> 0 OR Fatty_acids_total_polyunsaturated_g <> 0 OR Fatty_acids_total_saturated_g <> 0 OR Fatty_acids_total_trans_g <> 0 OR Fiber_insoluble_g <> 0 OR Fiber_soluble_g <> 0 OR Fiber_total_dietary_g <> 0 OR Folic_acid_mcg <> 0 OR Iodine_I_mcg <> 0 OR Iron_Fe_mg <> 0 OR Lactose_g <> 0 OR Magnesium_Mg_mg <> 0 OR Manganese_Mn_mg <> 0 OR Niacin_mg <> 0 OR Pantothenic_acid_mg <> 0 OR Phosphorus_P_mg <> 0 OR Potassium_K_mg <> 0 OR Protein_g <> 0 OR Riboflavin_mg <> 0 OR Selenium_Se_mcg <> 0 OR Sodium_Na_mg <> 0 OR Sugars_added_g <> 0 OR Sugars_total_g <> 0 OR Thiamin_mg <> 0 OR Total_lipid_fat_g <> 0 OR Total_sugar_alcohols_g <> 0 OR Vitamin_A_IU  <> 0 OR Vitamin_B12_mcg <> 0 OR Vitamin_B6_mg <> 0 OR Vitamin_C_total_ascorbic_acid_mg <> 0 OR Vitamin_D_IU <> 0 OR Vitamin_E_label_entry_primarily_IU <> 0 OR Vitamin_K_phylloquinone_mcg <> 0 OR Water_g <> 0 OR Xylitol_g <> 0 OR Zinc_Zn_mg <> 0)"
            cursor.execute(query)
            results = cursor.fetchall()
            return str(results[0])

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getIngredientBreakDown(self, connection, food):
        ''' returns all the ingredients in a given food item'''
        # ***contains method doesn't seem to be working - we want to see if the "long_name" OR branded food name contains the user input
        # i.e. user types in milk and query finds the rows containing milk in the food name column.
        food = food.upper()
        try:
            cursor = connection.cursor()
            query = "SELECT ingredients_english FROM Nutrek WHERE CONTAINS(long_name, " + str(food)+ ")"
            cursor.execute(query)
            results = cursor.fetchall()
            return str(results[0])

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getFoodAvailable(self, connection):
        '''returns all foods in database'''
        try:
            cursor = connection.cursor()
            query = "SELECT long_name FROM Nutrek"
            cursor.execute(query)
            results = cursor.fetchall()
            return str(results[0])

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def getAllNutrients(self, connection):
        '''returns all nutrients available in our database '''
        # ***thinking is a potentially deletable function?
        nutrients = list(self.data.columns.values)
        nutrients = nutrients[7:]
        #return nutrients
        results = cursor.fetchall()
        return str(results[0])


    def containsAllergen(self, connection, food, allergen):
        '''returns True if food contains allergen (could cause allergic reaction) and false if otherwise '''
        # ***how do we work with booleans in SQL? For example, we could find the food that contains key word of food enterered by user
        # but then we need to see if the ingredients adjacent to that food contain an allergen and output true OR false accordingly
        # if allergen in ingredients, then return True. Else (allergen not in ingredients list), return False.
        ingredients = list(self.getIngredientBreakDown(food)) # how can we call the getIntredientBreakdown method to use here now if it
        #is now using query
        food = food.upper()
        try:
            cursor = connection.cursor()
            query = "SELECT ingredients_english FROM Nutrek WHERE CONTAINS(long_name, " + str(food) + ")"
            cursor.execute(query)
            results = cursor.fetchall()
            return str(results[0])

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None



    def getNutrientThreshold(self, connection, food, nutrient, nutritionTarget):
        '''check if the amount of nutrients in a given food is meeting the indicated goal for a user'''
        # ***Conditions we are trying to apply to SQL: 1. nutrition columns each need to be above the nutrition target otherwise, it will output false. also
        # 2. the name of the food has to be valid and 3. the sum of the nutritents cannot be 0.
        food = food.upper()
        try:
            cursor = connection.cursor()
            query = "SELECT Ash_grams, Biotin_mcg, Caffeine_mg, Calcium_Ca_mg, Carbohydrate_by_difference_g, Carbohydrate_other_g, Cholesterol_mg, Chromium_Cr_mcg, Copper_Cu_mg, Fatty_acids_total_monounsaturated_g, Fatty_acids_total_polyunsaturated_g, Fatty_acids_total_saturated_g, Fatty_acids_total_trans_g, Fiber_insoluble_g, Fiber_soluble_g, Fiber_total_dietary_g, Folic_acid_mcg, Iodine_I_mcg, Iron_Fe_mg, Lactose_g, Magnesium_Mg_mg, Manganese_Mn_mg, Niacin_mg, Pantothenic_acid_mg, Phosphorus_P_mg, Potassium_K_mg, Protein_g, Riboflavin_mg, Selenium_Se_mcg, Sodium_Na_mg, Sugars_added_g, Sugars_total_g, Thiamin_mg, Total_lipid_fat_g, Total_sugar_alcohols_g, Vitamin_A_IU , Vitamin_B12_mcg, Vitamin_B6_mg, Vitamin_C_total_ascorbic_acid_mg, Vitamin_D_IU, Vitamin_E_label_entry_primarily_IU, Vitamin_K_phylloquinone_mcg, Water_g, Xylitol_g, Zinc_Zn_mg" + "FROM Nutrek" + "WHERE (long_name == " + str(food) + ") AND (Ash_grams <> 0 OR Biotin_mcg <> 0 OR Caffeine_mg <> 0 OR Calcium_Ca_mg <> 0 OR Carbohydrate_by_difference_g <> 0 OR Carbohydrate_other_g <> 0 OR Cholesterol_mg <> 0 OR Chromium_Cr_mcg <> 0 OR Copper_Cu_mg <> 0 OR Fatty_acids_total_monounsaturated_g <> 0 OR Fatty_acids_total_polyunsaturated_g <> 0 OR Fatty_acids_total_saturated_g <> 0 OR Fatty_acids_total_trans_g <> 0 OR Fiber_insoluble_g <> 0 OR Fiber_soluble_g <> 0 OR Fiber_total_dietary_g <> 0 OR Folic_acid_mcg <> 0 OR Iodine_I_mcg <> 0 OR Iron_Fe_mg <> 0 OR Lactose_g <> 0 OR Magnesium_Mg_mg <> 0 OR Manganese_Mn_mg <> 0 OR Niacin_mg <> 0 OR Pantothenic_acid_mg <> 0 OR Phosphorus_P_mg <> 0 OR Potassium_K_mg <> 0 OR Protein_g <> 0 OR Riboflavin_mg <> 0 OR Selenium_Se_mcg <> 0 OR Sodium_Na_mg <> 0 OR Sugars_added_g <> 0 OR Sugars_total_g <> 0 OR Thiamin_mg <> 0 OR Total_lipid_fat_g <> 0 OR Total_sugar_alcohols_g <> 0 OR Vitamin_A_IU  <> 0 OR Vitamin_B12_mcg <> 0 OR Vitamin_B6_mg <> 0 OR Vitamin_C_total_ascorbic_acid_mg <> 0 OR Vitamin_D_IU <> 0 OR Vitamin_E_label_entry_primarily_IU <> 0 OR Vitamin_K_phylloquinone_mcg <> 0 OR Water_g <> 0 OR Xylitol_g <> 0 OR Zinc_Zn_mg <> 0)"
            cursor.execute(query)
            results = cursor.fetchall()
            return str(results[0])

        except Exception as e:
            print ("Something went wrong when executing the query: ", e)
            return None

        pass

def main():
    # Connect to the database
    ds = Nutrek()
    connection = ds.connect()
    N = Nutrek()
    print(N.getNutrients('granola'))
    print(N.getIngredientBreakDown('granola'))
    print(N.containsAllergy('granola', 'peanuts'))


    # Disconnect from database
    ds.disconnect()
main()
