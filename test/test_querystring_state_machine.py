from unittest import TestCase

from state_machine import QuerystringStateMachine


class QuerystringStateMachineTestCase(TestCase):

    def setUp(self):
        self.state_machine = QuerystringStateMachine()

    def test_get_state(self):
        state = self.state_machine.get_state("initial", "filter")
        self.assertEqual("filter", state)

    def test_get_dynamic_state(self):
        state = self.state_machine.get_state("[where]", "[or]")
        self.assertEqual("{logical_operator:where}", state)
