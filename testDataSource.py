import unittest
from datasource import Nutrek

class DataSourceTester(unittest.TestCase):

    def setUp(self) -> None:
        self.nutrek = Nutrek()
        user = "odoome"
        password = "tiger672carpet"
        self.nutrek.connect(user, password)

    def testContainsAllergenBothValidInputs(self):
        food1 = "granola"
        allergen1 = "peanut"
        result1 = self.nutrek.containsAllergen(food1, allergen1)
        self.assertTrue(result1)

    def testContainsAllergenFirstInvalidInput(self):
        food2 = "aishee"
        allergen2 = "Milk"
        result2 = self.nutrek.containsAllergen(food2, allergen2)
        self.assertFalse(result2) 

    def testContainsAllergenSecondInvalidInput(self):
        food3 = "grain"
        allergen3 = "helicopter"
        result3 = self.nutrek.containsAllergen(food3, allergen3)
        self.assertFalse(result3)
    
    def testContainsAllergenBothInvalidInputs(self):
        food4 = "aishee"
        allergen4 = "helicopter"
        result4 = self.nutrek.containsAllergen(food4, allergen4)
        self.assertFalse(result4)

    def testcontainsAllergenFirstEmptyInput(self):
        food5 = ""
        allergen5 = "Lactose"
        result5 = self.nutrek.containsAllergen(food5, allergen5)
        self.assertIsNone(result5)
    
    def testcontainsAllergenSecondEmptyInput(self):
        food6 = "chicken"
        allergen6 = ""
        result6 = self.nutrek.containsAllergen(food6, allergen6)
        self.assertIsNone(result6)
    
    def testcontainsAllergenBothEmptyInputs(self):
        food7 = ""
        allergen7 = ""
        result7 = self.nutrek.containsAllergen(food7, allergen7)
        self.assertIsNone(result7)
                   
if __name__ == "__main__":
    unittest.main()
