from state_machine import END, StateMachine


class QuerystringStateMachine(StateMachine):

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
        validator = getattr(self, f"_is_valid_{validator_name}_state", None)
        return validator and validator(text)

    def _is_valid_value_state(self, text):
        return True

    def _is_valid_order_value_state(self, text):
        try:
            constraint, order = text.lower().split(" ")
            if self._is_valid_constraint_state(constraint):
                return order in {'asc', 'desc'}
        except ValueError:
            pass
        return False

    def _is_valid_logical_operator_state(self, text):
        return text in {"and", "or"}

    def _is_valid_relational_operator_state(self, text):
        return text in {"eq", "gt", "lt", "gte", "lte", "like", "nlike", "inq"}

    def _is_valid_integer_state(self, text):
        try:
            int(text)
        except ValueError:
            return False
        return True

    def _is_valid_constraint_state(self, text):
        if len(text.split(".")) == 2:
            return True
        return False
