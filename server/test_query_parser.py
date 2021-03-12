# # from src import query_parser
from query_parser import *


import unittest
class TestQueryParser(unittest.TestCase):

    def test_construct_condition(self):
        query = '"3"'
        self.assertEqual("3", construct_condition(query))

        query = "3"
        self.assertEqual(construct_condition(query), {"$regex":'.*3.*'})

        query = "<3"
        self.assertEqual(construct_condition(query), {"$lt":"3"})

        query = ">3"
        self.assertEqual(construct_condition(query), {"$gt":"3"})

    def test_construct_query(self):
        field = "price"
        query = ">3"
        expected = {"price":{"$gt":"3"}}
        self.assertEqual(expected, construct_query(field, query))

    def test_evaluate_logical(self):
        parsed = evaluate_logical('AND', ">3", "<3", "price")
        self.assertEqual(parsed, {'$and': [{'price': {'$gt': '3'}}, {'price': {'$lt': '3'}}]})
        
        parsed = evaluate_logical('NOT', "", "<3", "price")
        
        exprected = {"price":{"$not":{"$lt":"3"}}}
        self.assertEqual(exprected, parsed)

if __name__ == '__main__':
    unittest.main()