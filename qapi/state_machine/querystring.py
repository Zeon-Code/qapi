from collections import defaultdict

from qapi.state_machine import END, StateMachine

#TODO: Unit test covering all scenarios
class QuerystringStateValidation:
    def is_valid_value_state(self, text):
        return True

    def is_valid_order_value_state(self, text):
        try:
            constraint, order = text.lower().split(" ")
            if self.is_valid_constraint_state(constraint):
                return order in {'asc', 'desc'}
        except ValueError:
            pass
        return False

    def is_valid_logical_operator_state(self, text):
        return text in {"and", "or"}

    def is_valid_relational_operator_state(self, text):
        return text in {"eq", "gt", "lt", "gte", "lte", "like", "nlike", "inq"}

    def is_valid_integer_state(self, text):
        try:
            int(text)
        except ValueError:
            return False
        return True

    def is_valid_constraint_state(self, text):
        if len(text.split(".")) == 2:
            return True
        return False


class QuerystringStateMachine(StateMachine):

    state_validator = QuerystringStateValidation()

    states = {
        "initial": ["filter"],
        "filter": ["[where]", "[order]"],

        "[order]": ["{integer:order}"],
        "{integer:order}": ["{order_value}"],
        "{order_value}": [END],

        "[where]": ["{logical_operator:where}", "{constraint:where}"],
        "{logical_operator:where}": ["{integer:where}"],
        "{integer:where}": ["{constraint:where}"],
        "{constraint:where}": ["{relational_operator:where}", "{value}"],
        "{relational_operator:where}": ["{value}"],
        "{value}": [END]
    }

    def post_process(self, grouped_actions):
        where_actions = grouped_actions.actions.get("where", {}).values()
        if not where_actions:
            return

        for actions in list(where_actions):
            self._assemble_inq_operator(actions, grouped_actions)

    def get_state(self, previous_state, segment):
        return segment if segment in self.states else self._get_dynamic_state(previous_state, segment)

    def _get_dynamic_state(self, previous_state, segment):
        text = segment[1:-1] if segment.startswith("[") and segment.endswith("]") else segment
        for state in self.states[previous_state]:
            if self._is_valid(state, text):
                return state

    def _is_valid(self, state, text):
        dynamic_state_name = state[1:-1]
        validator_name = dynamic_state_name.split(':')[0] if dynamic_state_name.find(':') else dynamic_state_name
        validator = getattr(self.state_validator, f"is_valid_{validator_name}_state", None)
        return validator and validator(text)

    def _assemble_inq_operator(self, actions, grouped_actions):
        filtered_actions = defaultdict(list)
        for action in actions:
            key = f"{action.model}_{action.property}"
            if action.relational_operator == "inq":
                filtered_actions[key].append(action)

        if not filtered_actions:
            return

        for actions in filtered_actions.values():
            inq_action = actions[0].copy()
            inq_action.value = []
            for action in actions:
                inq_action.value.append(action.value)
                grouped_actions.delete(action)
            grouped_actions.add(inq_action)
