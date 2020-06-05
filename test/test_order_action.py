from unittest import TestCase

from action import OrderAction


class OrderActionTestCase(TestCase):
    def test_with_two_segments(self):
        action = OrderAction(["[0]", "model.property asc"])

        self.assertEqual(0, action.index)
        self.assertEqual("model", action.model)
        self.assertEqual("property", action.property)
        self.assertEqual("asc", action.value)
