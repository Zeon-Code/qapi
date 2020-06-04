from unittest import TestCase

from parser import Parser


class ParseTestCase(TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_parse_where_logical_operator_and(self):
        pass

    def test_parse_where_logical_operator_or(self):
        pass

    def test_parse_where_condition(self):
        querystring = {"filter[where][table.column]": "value"}
        operations = self.parser.parse(querystring)
        self.assertTrue(operations)
