from unittest import TestCase

from parser import Parser


class ParseTestCase(TestCase):

    def setUp(self):
        self.parser = Parser()

    def test_where_condition(self):
        querystring = {"filter[where][table.column]": "value"}
        operations = self.parser.parse(querystring)
        self.assertEqual(1, len(operations))

    def test_multiples_where_condition(self):
        querystring = {
            "filter[where][table.column1]": "value1",
            "filter[where][table.column2]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_logical_operator_and(self):
        querystring = {
            "filter[where][and][0][table.column1]": "value1", 
            "filter[where][and][0][table.column2]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_logical_operator_or(self):
        querystring = {
            "filter[where][or][0][table.column1]": "value1", 
            "filter[where][or][0][table.column2]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_eq(self):
        querystring = {"filter[where][table.column][eq]": "value"}
        operations = self.parser.parse(querystring)
        self.assertEqual(1, len(operations))

    def test_where_relational_operator_eq_with_logical_operator_and(self):
        querystring = {
            "filter[where][and][0][table.column1][eq]": "value1",
            "filter[where][and][0][table.column2][eq]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_eq_with_logical_operator_or(self):
        querystring = {
            "filter[where][or][0][table.column1][eq]": "value1",
            "filter[where][or][0][table.column2][eq]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_lt(self):
        querystring = {"filter[where][table.column][lt]": "value"}
        operations = self.parser.parse(querystring)
        self.assertEqual(1, len(operations))

    def test_where_relational_operator_lt_with_logical_operator_and(self):
        querystring = {
            "filter[where][and][0][table.column1][lt]": "value1",
            "filter[where][and][0][table.column2][lt]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_lt_with_logical_operator_or(self):
        querystring = {
            "filter[where][or][0][table.column1][lt]": "value1",
            "filter[where][or][0][table.column2][lt]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_lte(self):
        querystring = {"filter[where][table.column][lte]": "value"}
        operations = self.parser.parse(querystring)
        self.assertEqual(1, len(operations))

    def test_where_relational_operator_lte_with_logical_operator_and(self):
        querystring = {
            "filter[where][and][0][table.column1][lte]": "value1",
            "filter[where][and][0][table.column2][lte]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_lte_with_logical_operator_or(self):
        querystring = {
            "filter[where][or][0][table.column1][lte]": "value1",
            "filter[where][or][0][table.column2][lte]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_gt(self):
        querystring = {"filter[where][table.column][gt]": "value"}
        operations = self.parser.parse(querystring)
        self.assertEqual(1, len(operations))

    def test_where_relational_operator_gt_with_logical_operator_and(self):
        querystring = {
            "filter[where][and][0][table.column1][gt]": "value1",
            "filter[where][and][0][table.column2][gt]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_gt_with_logical_operator_or(self):
        querystring = {
            "filter[where][or][0][table.column1][gt]": "value1",
            "filter[where][or][0][table.column2][gt]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_gte(self):
        querystring = {"filter[where][table.column][gte]": "value"}
        operations = self.parser.parse(querystring)
        self.assertEqual(1, len(operations))

    def test_where_relational_operator_gte_with_logical_operator_and(self):
        querystring = {
            "filter[where][and][0][table.column1][gte]": "value1",
            "filter[where][and][0][table.column2][gte]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_gte_with_logical_operator_or(self):
        querystring = {
            "filter[where][or][0][table.column1][gte]": "value1",
            "filter[where][or][0][table.column2][gte]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_like(self):
        querystring = {"filter[where][table.column][like]": "value"}
        operations = self.parser.parse(querystring)
        self.assertEqual(1, len(operations))

    def test_where_relational_operator_like_with_logical_operator_and(self):
        querystring = {
            "filter[where][and][0][table.column1][like]": "value1",
            "filter[where][and][0][table.column2][like]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_like_with_logical_operator_or(self):
        querystring = {
            "filter[where][or][0][table.column1][like]": "value1",
            "filter[where][or][0][table.column2][like]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_nlike(self):
        querystring = {"filter[where][table.column][nlike]": "value"}
        operations = self.parser.parse(querystring)
        self.assertEqual(1, len(operations))

    def test_where_relational_operator_nlike_with_logical_operator_and(self):
        querystring = {
            "filter[where][and][0][table.column1][nlike]": "value1",
            "filter[where][and][0][table.column2][nlike]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_nlike_with_logical_operator_or(self):
        querystring = {
            "filter[where][or][0][table.column1][nlike]": "value1",
            "filter[where][or][0][table.column2][nlike]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_inq(self):
        querystring = {"filter[where][table.column][inq]": "value"}
        operations = self.parser.parse(querystring)
        self.assertEqual(1, len(operations))

    def test_where_relational_operator_inq_with_logical_operator_and(self):
        querystring = {
            "filter[where][and][0][table.column1][inq]": "value1",
            "filter[where][and][0][table.column2][inq]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_where_relational_operator_inq_with_logical_operator_or(self):
        querystring = {
            "filter[where][or][0][table.column1][inq]": "value1",
            "filter[where][or][0][table.column2][inq]": "value2"
        }
        operations = self.parser.parse(querystring)
        self.assertEqual(2, len(operations))

    def test_order(self):
        querystring = {"filter[order][0]": "table.column asc"}
        operations = self.parser.parse(querystring)
        self.assertEqual(1, len(operations))
