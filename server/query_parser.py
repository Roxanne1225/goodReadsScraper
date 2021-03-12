import sys
import os
import re
from dotenv import load_dotenv
from dataCollection import DataCollection

def print_error_and_exit_no_field(field):
    print("Document does not have the " + field + " field")
    sys.exit(1)

def get_documnet_field(document, field):
    if not field in document:
        print_error_and_exit_no_field(field)
    return document[field]

def field_contains(document, field, target):
    if not field in document:
        print_error_and_exit_no_field(field)
    return str(target) in str(document[field])

def field_matches(document, field, target):
    if not field in document:
        print_error_and_exit_no_field(field)
    return str(target) == str(document[field])

load_dotenv()
MONGO_CONNECTION_STRING = os.getenv('MONGO_CONNECTION_STRING')

book_data_collection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", 'book')
author_data_collection = DataCollection(MONGO_CONNECTION_STRING, "goodReads", 'author')

AND = 'AND'
OR = 'OR'
NOT = 'NOT'
logical_operators = [AND, OR, NOT]

def eval_query(query):
    if ':' not in query:
        return None
    for i in range(len(query)):
        if(query[i] == ':'):
            left_str = query[:i]
            right_str = query[i+1:]
            return colon_operator(left_str, right_str)


def colon_operator(left_str, right_str):
    if '.' not in left_str:
        print("invalid")
    else:
        index = left_str.index('.')
        data_collection = left_str[:index]
        field = left_str[index+1:]
        conditions = construct_query(field, right_str)
        if data_collection == 'book':
            return book_data_collection.find_by_query(conditions)
        else:
            return author_data_collection.find_by_query(conditions)

        # return data_collection.find_all(conditions)

def construct_query(field, query):
    if len(query) == 0:
        print("empty query")
        return ""
    query_list = query.split(" ")
    for operator in logical_operators:
        if operator in query_list:
            index = query_list.index(operator)
            left_str = " ".join(query_list[:index])
            right_str = " ".join(query_list[index+1:])
            return evaluate_logical(operator, left_str, right_str, field)

    conditions = construct_condition(query)
    return {field:conditions}

def construct_condition(query):
    if query.find('"') != -1:
        reg = '"(.*)"'
        exact_value = re.search(reg, query).group(1)
        return exact_value
    
    if query.find("<") != -1:
        reg = '<(.*)'
        exact_value = re.search(reg, query).group(1)
        return {'$lt' : exact_value}
    
    if query.find(">") != -1:
        reg = '>(.*)'
        exact_value = re.search(reg, query).group(1)
        return {'$gt' : exact_value}


    return {'$regex': ".*" + query + ".*"}

def evaluate_logical(operator, left_str, right_str, field):
    parsed_right = construct_query(field, right_str)
    if operator == NOT:
        return {field : {"$not": construct_condition(right_str)}}
    parsed_left = construct_query(field, left_str)
    if operator == AND:
        return { "$and" : [parsed_left, parsed_right]}
    else:
        return { "$or" : [parsed_left, parsed_right]}




