import unittest
from movie_comparer import MovieComparer

class TestCheapestPrice(unittest.TestCase):

    def test_present_in_both_db(self):
        """ Test title, which are present in both databases
        """
        movie_comparer = MovieComparer()
        price = movie_comparer.get_cheapest(1)
        self.assertTrue(price == 900.5)

    def test_present_in_one_db(self):
        """ Test title, which is present in one database only
        """
        movie_comparer = MovieComparer()
        price = movie_comparer.get_cheapest(7)
        self.assertTrue(price == 129.5)

    def test_not_present_in_any_db(self):
        """ Test title, which is not present in any database
        """
        movie_comparer = MovieComparer()
        price = movie_comparer.get_cheapest(9)
        self.assertTrue(price == None)

    def test_invalid_index(self):
        """ Test invalid index
        """
        movie_comparer = MovieComparer()
        price = movie_comparer.get_cheapest('ab')
        self.assertTrue(price == None)

if __name__ == '__main__':
	unittest.main()
