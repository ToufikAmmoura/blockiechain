import unittest

"""
maakt niet uit hoeveel functies we hebben, we gaan er voor elke een testfunctie schrijven hierin
het hele systeem zal werkend zijn
"""


class TestIt(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum([1,2,3]), 6, 'should be 6')
    
if __name__ == '__main__':
    unittest.main()