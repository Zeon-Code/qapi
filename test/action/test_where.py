
from unittest import TestCase

from qapi.action import WhereAction


class WhereActionTestCase(TestCase):

    def test_copy(self):
        action1 = WhereAction(["[model.property]", "value"])
        action2 = action1.copy()
        action2.value = "value2"

        self.assertNotEqual(action1.value, action2.value)
        self.assertNotEqual(id(action1), id(action2))

    def test_with_two_segments(self):
        action = WhereAction(["[model.property]", "value"])

        self.assertEqual(None, action.index)
        self.assertEqual(None, action.logical_operator)
        self.assertEqual("eq", action.relational_operator)
        self.assertEqual("model", action.model)
        self.assertEqual("property", action.property)
        self.assertEqual("value", action.value)

    def test_with_three_segments(self):
        action = WhereAction(["[model.property]", "[lt]", "value"])

        self.assertEqual(None, action.index)
        self.assertEqual(None, action.logical_operator)
        self.assertEqual("lt", action.relational_operator)
        self.assertEqual("model", action.model)
        self.assertEqual("property", action.property)
        self.assertEqual("value", action.value)

    def test_with_four_segments(self):
        action = WhereAction(["[and]", "[0]", "[model.property]", "value"])

        self.assertEqual(0, action.index)
        self.assertEqual("and", action.logical_operator)
        self.assertEqual("eq", action.relational_operator)
        self.assertEqual("model", action.model)
        self.assertEqual("property", action.property)
        self.assertEqual("value", action.value)

    def test_with_five_segments(self):
        action = WhereAction(["[and]", "[0]", "[model.property]", "[gte]", "value"])

        self.assertEqual(0, action.index)
        self.assertEqual("and", action.logical_operator)
        self.assertEqual("gte", action.relational_operator)
        self.assertEqual("model", action.model)
        self.assertEqual("property", action.property)
        self.assertEqual("value", action.value)
