from unittest import TestCase

from qapi.state_machine import QuerystringStateMachine, QuerystringStateValidation


class QuerystringStateMachineTestCase(TestCase):

    def setUp(self):
        self.state_machine = QuerystringStateMachine()

    def test_get_state(self):
        state = self.state_machine.get_state("initial", "filter")
        self.assertEqual("filter", state)

    def test_get_dynamic_state(self):
        state = self.state_machine.get_state("[where]", "[or]")
        self.assertEqual("{logical_operator:where}", state)


class QuerystringStateValidationTestCase(TestCase):

    def setUp(self):
        self.validator = QuerystringStateValidation()

    def test_value_with_none(self):
        is_valid = self.validator.is_valid_value_state(None)
        self.assertTrue(is_valid)

    def test_value_with_int(self):
        is_valid = self.validator.is_valid_value_state(0)
        self.assertTrue(is_valid)

    def test_value_with_double(self):
        is_valid = self.validator.is_valid_value_state(1.5)
        self.assertTrue(is_valid)

    def test_value_with_string(self):
        is_valid = self.validator.is_valid_value_state("")
        self.assertTrue(is_valid)

    def test_value_with_list(self):
        is_valid = self.validator.is_valid_value_state([])
        self.assertTrue(is_valid)

    def test_value_with_dict(self):
        is_valid = self.validator.is_valid_value_state({})
        self.assertTrue(is_valid)

    def test_value_with_set(self):
        is_valid = self.validator.is_valid_value_state(set())
        self.assertTrue(is_valid)

    def test_order_value_with_asc(self):
        is_valid = self.validator.is_valid_order_value_state("model.property asc")
        self.assertTrue(is_valid)

    def test_order_value_with_desc(self):
        is_valid = self.validator.is_valid_order_value_state("model.property desc")
        self.assertTrue(is_valid)

    def test_order_value_with_wrong_values(self):
        is_valid = self.validator.is_valid_order_value_state("wrongvalue")
        self.assertFalse(is_valid)

        is_valid = self.validator.is_valid_order_value_state("wrongvalue someorder")
        self.assertFalse(is_valid)

    def test_logical_operator_and(self):
        is_valid = self.validator.is_valid_logical_operator_state("and")
        self.assertTrue(is_valid)

    def test_logical_operator_or(self):
        is_valid = self.validator.is_valid_logical_operator_state("or")
        self.assertTrue(is_valid)

    def test_relational_operator_eq(self):
        is_valid = self.validator.is_valid_relational_operator_state("eq")
        self.assertTrue(is_valid)

    def test_relational_operator_lt(self):
        is_valid = self.validator.is_valid_relational_operator_state("lt")
        self.assertTrue(is_valid)

    def test_relational_operator_lte(self):
        is_valid = self.validator.is_valid_relational_operator_state("lte")
        self.assertTrue(is_valid)

    def test_relational_operator_gt(self):
        is_valid = self.validator.is_valid_relational_operator_state("gt")
        self.assertTrue(is_valid)

    def test_relational_operator_gte(self):
        is_valid = self.validator.is_valid_relational_operator_state("gte")
        self.assertTrue(is_valid)

    def test_relational_operator_inq(self):
        is_valid = self.validator.is_valid_relational_operator_state("inq")
        self.assertTrue(is_valid)

    def test_relational_operator_like(self):
        is_valid = self.validator.is_valid_relational_operator_state("like")
        self.assertTrue(is_valid)

    def test_relational_operator_nlike(self):
        is_valid = self.validator.is_valid_relational_operator_state("nlike")
        self.assertTrue(is_valid)

    def test_integer(self):
        is_valid = self.validator.is_valid_integer_state("1")
        self.assertTrue(is_valid)

    def test_not_integer(self):
        is_valid = self.validator.is_valid_integer_state("aa")
        self.assertFalse(is_valid)

    def test_constraint(self):
        is_valid = self.validator.is_valid_constraint_state("model.property")
        self.assertTrue(is_valid)
