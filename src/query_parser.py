import sys

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


