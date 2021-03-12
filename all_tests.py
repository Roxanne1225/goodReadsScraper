import unittest
from testDataCollection import TestDataCollection
from test_query_parser import TestQueryParser
from testScraper import TestScraper

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestScraper))
    suite.addTest(unittest.makeSuite(TestQueryParser))
    suite.addTest(unittest.makeSuite(TestDataCollection))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())