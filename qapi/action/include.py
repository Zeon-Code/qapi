from qapi.action import Action


class IncludeAction(Action):

    type = "include"

    @property
    def context(self):
        return None

    def __init__(self, segments):
        if len(segments) == 1:
            self.model = self._get_text(segments[0])

    def copy(self):
        return IncludeAction([
            self.model
        ])
