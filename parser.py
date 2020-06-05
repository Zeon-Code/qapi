

END = "end"


class Operation:
    def __init__(self, segments):
        self._segments = segments


class Parser:

    states = {
        "initial": {"filter"},
        "filter": {"[where]", "[order]"},

        "[order]": {"{integer:order}"},
        "{integer:order}": {END},

        "[where]": {"{logical_operator:where}", "{constraint:where}"},
        "{logical_operator:where}": {"{integer:where}"},
        "{integer:where}": {"{constraint:where}"},
        "{constraint:where}": {"{relational_operator}", END},
        "{relational_operator}": {END}
    }

    def parse(self, querstring):
        operations = []
        for _key, _ in querstring.items():
            key = _key.lower()
            segments = self._segment_key(key)
            if self._validate_segments(segments):
                operation = Operation(segments)
                operations.append(operation)
        return operations

    def _segment_key(self, key):
        raw = key
        segments = []

        while raw:
            match_index = raw.find("[", 1)
            if match_index > 0:
                segments.append(raw[:match_index])
                raw = raw[match_index:]
                continue

            segments.append(raw)
            raw = ""
        return segments

    def _validate_segments(self, segments):
        previous_state = "initial"
        for segment in segments:
            state = self._get_state(previous_state, segment)
            if state not in self.states or state not in self.states[previous_state]:
                return False
            previous_state = state
        return END in self.states[previous_state]

    def _get_state(self, previous_state, segment):
        return segment if segment in self.states else self._get_dynamic_state(previous_state, segment)

    def _get_dynamic_state(self, previous_state, segment):
        text = segment[1:-1] if segment.startswith("[") and segment.endswith("]") else segment
        for state in self.states[previous_state]:
            space_name = state[1:-1] if state.startswith("{") and state.endswith("}") else state
            validator_name = space_name.split(':')[0] if space_name.find(':') else space_name
            validator = getattr(self, f"_is_valid_{validator_name}_state", None)
            if validator and validator(text):
                return state

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