

class Action:

    @property
    def context(self):
        raise NotImplementedError()

    def _parse_constraint(self, constraint):
        return self._get_text(constraint).split(".")

    def _parse_index(self, index):
        return int(self._get_text(index))

    def _get_text(self, segment):
        return segment[1:-1] if segment.startswith("[") and segment.endswith("]") else segment


from action.order import OrderAction
from action.where import WhereAction
from action.group import ActionGroup


def get_action(_segments):
    _type, command = _segments[0:2]
    segments = _segments[2:]

    if _type == "filter" and command == "[order]":
        return OrderAction(segments)
    elif _type == "filter" and command == "[where]":
        return WhereAction(segments)
