import psycopg2
import getpass
import pandas as pd
'''Our dataset was too big to upload on github so we used the pandas, a data science library for
our manipulation purposed. The dataset is zipped on github now.'''
class Nutrek:
    def __init__(self):
        ''' Nutrek executes all of the queries on the database
            and formats the data to send back to the front end'''
        self.data  = pd.read_csv("FullDataSet.csv")

    def getNutrients(self, food):
        ''' returns all the nutrients and in
           a given food item '''
        food = food.upper()
        food = self.getFoodAvailable(food)
        food = food.iloc[0]
        nutrients = self.data.loc[self.data['ingredients_english'] == food]
        nutrient_list  = self.data[self.data['long_name'].str.match(food)]
        nutrient_dictionary = {}
        for index, nutrient in nutrient_list.iterrows():
            nutrient_dictionary[index] = nutrient
        return nutrient_dictionary

    def getIngredientBreakDown(self, food):
        ''' returns all the ingredients in a given food item'''
        food = food.upper()
        foods = self.getFoodAvailable(food)
        foods = self.getFoodAvailable(food).iloc[0]
        if len(foods) == 0:
            return None
        nutrients = self.data['ingredients_english']
        food = self.data['long_name']
        new_data = pd.DataFrame(self.data, columns=['long_name', 'ingredients_english'])
        rows = {}
        for index, row in new_data.iterrows():
            rows[row.long_name] = [row.ingredients_english]
        for item in rows:
            if foods in item or item in foods:
                return rows[foods]

    def getFoodAvailable(self, food):
        '''returns all the foods in our database'''
        food = food.upper()
        foodItems = self.data['long_name'].str.find(food)
        foodAvailable = self.data['long_name'][foodItems>0]
        return foodAvailable

    def getAllNutrients(self):
        '''returns all nutrients available in our database '''
        nutrients = list(self.data.columns.values)
        nutrients = nutrients[7:]
        return nutrients


    def containsAllergen(self, food, allergen):
        '''returns True if food can cause allergic reactions
            and false otherwise'''
        ingredients = list(self.getIngredientBreakDown(food))
        allergen = allergen.upper()
        if ingredients == []:
            return False
        elif allergen in ingredients:
            return True
        else:
            for ingredient in ingredients:
                if allergen in ingredient:
                    return True
            return False


    def getNutrientThreshold(self, food, nutrient, goal):
        '''check if a given nutrient in a given
            food is meeting the goal for the person'''
        pass

N = Nutrek()
print(N.getNutrients('granola'))
# print(N.getIngredientBreakDown('granola'))
# print(N.containsAllergy('granola', 'peanuts'))
