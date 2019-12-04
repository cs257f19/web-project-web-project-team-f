import unittest
from datasource import Nutrek


class DataSourceTester(unittest.TestCase):

    def setUp(self) -> None:
        self.nutrek = Nutrek()
        user = 'odoome'
        password = 'tiger672carpet'
        self.nutrek.connect(user, password)

    def test_containsAllergen_bothValidInputs(self):
        food1 = 'granola'
        allergen1 = 'peanut'
        result1 = self.nutrek.containsAllergen(food1, allergen1)
        self.assertTrue(result1)
       

    def test_containAllergen_firstInValidInput(self):
        food2 = 'milk'
        allergen2 = 'Chairs'
        result2 = self.nutrek.containsAllergen(food2, allergen2)
        self.assertFalse(result2) 

    def test_containsAllergen_secondInvalidInput(self):
        food3 = 'grain'
        allergen3 = 'helicopter'
        result3 = self.nutrek.containsAllergen(food3, allergen3)
        self.assertFalse(result3)
    
    def test_containsAllergen_emptyInput1(self):
        food4 = ""
        allergen4 = "Lactose"
        result4 = self.nutrek.containsAllergen(food4, allergen4)
       
        

if __name__ == '__main__':
    unittest.main()
