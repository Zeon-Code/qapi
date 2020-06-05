from unittest import TestCase

from action import ActionGroup, WhereAction, OrderAction


class ActionGroupTestCase(TestCase):

    def setUp(self):
        self.group = ActionGroup()

    def test_add(self):
        action = WhereAction(["[model.property]", "value"])
        self.assertEqual(0, self.group.total)
        self.group.add(action)        
        self.assertEqual(1, self.group.total)
        self.assertEqual(
            {'where': {'main': [action]}}, 
            self.group.actions
        )

    def test_del(self):
        action = WhereAction(["[and]", "[0]", "[model.property]", "value"])
        self.assertEqual(0, self.group.total)
        self.group.add(action)
        self.group.delete(action)        
        self.assertEqual(0, self.group.total)
        self.assertEqual({}, self.group.actions)
