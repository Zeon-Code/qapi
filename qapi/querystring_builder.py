from qapi.action import get_action, ActionGroup
from qapi.state_machine import END, QuerystringStateMachine


class QueryStringBuilder:
    def __init__(self):
        self.state_machine = QuerystringStateMachine()

    #TODO: do not overwrite key (key = _key.lower())
    def parse(self, querystring):
        grouped_actions = ActionGroup()
        self.state_machine.pre_process(grouped_actions)
        for _key, value in querystring:
            key = _key.lower()
            segments = self._segment_key(key)
            segments.append(value)
            if self._validate_segments(segments):
                grouped_actions.add(get_action(segments))

        self.state_machine.post_process(grouped_actions)
        return grouped_actions

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
            state = self.state_machine.get_state(previous_state, segment)
            if not self.state_machine.exist(state) or not self.state_machine.exist_in(previous_state, state):
                return False
            previous_state = state
        return self.state_machine.exist_in(previous_state, END)
