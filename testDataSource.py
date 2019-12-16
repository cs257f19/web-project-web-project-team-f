import unittest
from datasource import Nutrek

class DataSourceTester(unittest.TestCase):

    def setUp(self) -> None:
        self.nutrek = Nutrek()
        user = "odoome"
        password = "tiger672carpet"
        self.nutrek.connect(user, password)

    '''allergen is in valid food name'''
    def testContainsAllergenBothValidInputs(self):
        food1 = "granola"
        allergen1 = "peanut"
        result1 = self.nutrek.containsAllergen(food1, allergen1)
        self.assertTrue(result1)
    
    '''allergen is not in valid food name'''
    def testContainsAllergenFirstInvalidInput(self):
        food2 = "grain"
        allergen2 = "helicopters"
        result2 = self.nutrek.containsAllergen(food2, allergen2)
        self.assertFalse(result2) 

    '''food name is not valid (not empty)'''
    def testContainsAllergenSecondInvalidInput(self):
        food3 = "aishee"
        allergen3 = "peanut"
        result3 = self.nutrek.containsAllergen(food3, allergen3)
        self.assertIsNone(result3)
   
    '''food name is empty'''
    def testContainsAllergenFirstEmptyInput(self):
        food4 = ""
        allergen4 = "Lactose"
        result4 = self.nutrek.containsAllergen(food4, allergen4)
        self.assertIsNone(result4)
    
    '''allergen is empty'''
    def testContainsAllergenSecondEmptyInput(self):
        food5 = "chicken"
        allergen5 = ""
        result5 = self.nutrek.containsAllergen(food5, allergen5)
        self.assertIsNone(result5)
    
    '''food and allergen both empty'''
    def testContainsAllergenBothEmptyInputs(self):
        food6 = ""
        allergen6 = ""
        result6 = self.nutrek.containsAllergen(food6, allergen6)
        self.assertIsNone(result6)
                   
if __name__ == "__main__":
    unittest.main()
