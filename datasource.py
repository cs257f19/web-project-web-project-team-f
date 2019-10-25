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
        ''' returns all the nutrients in
           a given food item '''
        food = food.upper()
        food = self.getFoodAvailable(food)
        food = food.iloc[10]
        nutrients = self.data.loc[self.data['long_name'] == food]
        return nutrients

    def getFoodAvailable(self, food):
        '''returns all types of said food in our database'''
        food = food.upper()
        foodItems = self.data['long_name'].str.find(food)
        foodAvailable = self.data['long_name'][foodItems>0]
        return foodAvailable

    def getAllNutrients(self):
        '''returns all nutrients we keep track of in out database '''
        nutrients = list(self.data.columns.values)
        nutrients = nutrients[7:]
        return nutrients


    def containsAllergy(self, food, allergy):
        '''returns True if food can cause allergic reactions
            and false otherwise'''
        food = food.upper()
        food = self.getFoodAvailable(food)
        pass



    def getNutrientThreshold(self, food, nutrient, goal):
        '''check if a given nutrient in a given
            food is meeting the goal for the person'''

    def getIngredientBreakDown(self, food):
        '''Get all ingredients in a food '''
        pass






'''Testing '''
N = Nutrek()
print(N.getFoodAvailable('beef'))
#print(N.containsAllergy('beef', 'lactose'))
print(N.getNutrients('beef'))
print(N.getAllNutrients())
