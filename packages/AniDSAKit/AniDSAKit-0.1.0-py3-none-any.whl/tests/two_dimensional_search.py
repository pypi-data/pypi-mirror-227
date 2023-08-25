import unittest
from searching_algorithm.two_dimensional_search import TwoDSearch

class TwoDSearchTest(unittest.TestCase):
    
    def setUp(self):
        self.search_algorithm = TwoDSearch()
    
    def test_twoD_search_found(self):
        matrix = [[1,3,7,5], [10, 11, 16, 20], [23 , 30, 34, 60]]
        target = 3
        result = self.search_algorithm.search(matrix,target)
        assert result == True, f"Test case 1 failed. Expected True but got {result}"
    
    def test_twoD_search_not_found(self):
        matrix = [[1,3,7,5], [10, 11, 16, 20], [23 , 30, 34, 60]]
        target = 80
        result = self.search_algorithm.search(matrix,target)
        assert result == False, f"Test case 2 failed. Expected False but got {result}"


if __name__ == "__main__":
    unittest.main()