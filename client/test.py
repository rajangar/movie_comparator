import unittest
import time
from movie_client import find_cheapest_price

class TestCheapestPrice(unittest.TestCase):

    def test_present_in_both_db(self):
        """ Test title, which are present in both databases
        """
        for i in range(5):
            price = find_cheapest_price("Star Wars: Episode VI - Return of the Jedi")
            if price is "69.5":
                break
            time.sleep(1)
        self.assertTrue(price == "69.5")

    def test_present_in_one_db(self):
        """ Test title, which is present in one database only
        """
        for i in range(5):
            price = find_cheapest_price("Star Wars: The Force Awakens")
            if price is "129.5":
                break
            time.sleep(1)
        self.assertTrue(price == "129.5")

    def test_not_present_in_any_db(self):
        """ Test title, which is not present in any database
        """
        price = find_cheapest_price("Only Star Wars")
        self.assertTrue(price == None)

    def test_extra_initial_spaces(self):
        """ Test extra initial spaces
        """
        for i in range(5):
            price = find_cheapest_price("   Star Wars: Episode VI - Return of the Jedi")
            if price is "69.5":
                break
            time.sleep(1)
        self.assertTrue(price == "69.5")

    def test_extra_end_spaces(self):
        """ Test extra end spaces
        """
        for i in range(5):
            price = find_cheapest_price("Star Wars: Episode VI - Return of the Jedi   ")
            if price is "69.5":
                break
            time.sleep(1)
        self.assertTrue(price == "69.5")

    def test_extra_between_spaces(self):
        """ Test extra between spaces
        """
        for i in range(5):
            price = find_cheapest_price("Star Wars:    Episode VI - Return of the Jedi   ")
            if price is not None:
                break
            time.sleep(1)
        self.assertTrue(price == None)

    def test_small_letters(self):
        """ Test title with all small letters
        """
        for i in range(5):
            price = find_cheapest_price("star wars: episode VI - return of the jedi")
            if price is "69.5":
                break
            time.sleep(1)
        self.assertTrue(price == "69.5")

    def test_capital_letters(self):
        """ Test title with all capital letters
        """
        for i in range(5):
            price = find_cheapest_price("STAR WARS: EPISODE VI - RETURN OF THE JEDI")
            if price is "69.5":
                break
            time.sleep(1)
        self.assertTrue(price == "69.5")

if __name__ == '__main__':
	unittest.main()
