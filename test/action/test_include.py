from unittest import TestCase

from qapi.action import IncludeAction


class IncludeActionTestCase(TestCase):
    def test_with_two_segments(self):
        action = IncludeAction(["model"])

        self.assertEqual(None, action.context)
        self.assertEqual("model", action.model)

    def test_copy(self):
        action1 = IncludeAction(["model1"])
        action2 = action1.copy()
        action2.model = "model2"

        self.assertNotEqual(action1.model, action2.model)
        self.assertNotEqual(id(action1), id(action2))
