from unittest import TestCase

from qapi.action import OrderAction


class OrderActionTestCase(TestCase):
    def test_with_two_segments(self):
        action = OrderAction(["[0]", "model.property asc"])

        self.assertEqual(0, action.index)
        self.assertEqual("model", action.model)
        self.assertEqual("property", action.property)
        self.assertEqual("asc", action.value)

    def test_copy(self):
        action1 = OrderAction(["[0]", "model.property asc"])
        action2 = action1.copy()
        action2.value = "desc"

        self.assertNotEqual(action1.value, action2.value)
        self.assertNotEqual(id(action1), id(action2))
