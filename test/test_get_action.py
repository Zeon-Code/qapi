from unittest import TestCase

from action import get_action, WhereAction, OrderAction


class GetActionTestCase(TestCase):
    def test_where_filter_with_2_segments(self):
        action = get_action(["filter", "[where]", "[model.property]", "value"])
        self.assertIsInstance(action, WhereAction)

    def test_where_filter_with_four_segments(self):
        action = get_action(["filter", "[where]", "[and]", "[0]", "[model.property]", "value"])
        self.assertIsInstance(action, WhereAction)

    def test_where_filter_with_five_segments(self):
        action = get_action(["filter", "[where]", "[and]", "[0]", "[model.property]", "[lt]", "value"])
        self.assertIsInstance(action, WhereAction)

    def test_order_filter_with_five_segments(self):
        action = get_action(["filter", "[order]", "[0]", "model.property asc"])
        self.assertIsInstance(action, OrderAction)
