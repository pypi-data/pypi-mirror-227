import unittest
from searching_algorithm.ternary_search import TernarySearch

class TernarySearchTest(unittest.TestCase):
    
    def setUp(self):
        self.search_algorithm = TernarySearch()
    
    def test_ternary_search_found(self):
        arr = [1,2,3,4,5,6,7,8,9]
        target = 5
        result = self.search_algorithm.search(arr,target)
        assert result == 4, f"Test case 1 failed. Expected 4 but got {result}"

    def test_ternary_search_not_found(self):
        arr = [1,2,3,4,5,6,7,8,9]
        target = 10
        result = self.search_algorithm.search(arr,target)
        assert result == -1, f"Test case 2 failed. Expected -1 but got {result}"
        

if __name__ == "__main__":
    unittest.main()