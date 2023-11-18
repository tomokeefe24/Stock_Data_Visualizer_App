import unittest
import app


class TestApp(unittest.TestCase):

    def test_getSymbols(self):
        list = app.getSymbols()
        for i in list:
            print(i)

    
    """
    def test_add(self):
        self.assertEqual(calc.add(10, 5), 15)
        self.assertEqual(calc.add(-10, 5), -5)
        self.assertEqual(calc.add(-10, -5), -15)

    def test_subtract(self):
        self.assertEqual(calc.subtract(10,5), 5)
    
    def test_multiply(self):
        self.assertEqual(calc.multiply(4,5), 20)
    """

if __name__ == '__main__':
    unittest.main()