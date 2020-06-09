from unittest import TestCase

from qapi.action import get_action, WhereAction, OrderAction, IncludeAction


class GetActionTestCase(TestCase):
    def test_where_filter(self):
        action = get_action(["filter", "[where]", "[model.property]", "value"])
        self.assertIsInstance(action, WhereAction)

    def test_order_filter(self):
        action = get_action(["filter", "[order]", "[0]", "model.property asc"])
        self.assertIsInstance(action, OrderAction)

    def test_include_filter(self):
        action = get_action(["filter", "[include]", "model"])
        self.assertIsInstance(action, IncludeAction)
