from action import Action


class WhereAction(Action):

    type = "where"

    @property
    def context(self):
        context = "main"
        if self.logical_operator or self.index:
            context = f"{self.logical_operator}_{self.index}"
        return context

    def __init__(self, segments):
        self.index = None
        self.logical_operator = None
        self.relational_operator = "eq"
        self.value = segments[-1]
        
        if len(segments) == 2:
            self.model, self.property = self._parse_constraint(segments[0])

        elif len(segments) == 3:
            self.model, self.property = self._parse_constraint(segments[0])
            self.relational_operator = self._get_text(segments[1])

        elif len(segments) == 4:
            self.logical_operator = self._get_text(segments[0])
            self.index = self._parse_index(segments[1])
            self.model, self.property = self._parse_constraint(segments[2])
        
        elif len(segments) == 5:
            self.logical_operator = self._get_text(segments[0])
            self.index = self._parse_index(segments[1])
            self.model, self.property = self._parse_constraint(segments[2])
            self.relational_operator = self._get_text(segments[3])


    def copy(self):
        action = WhereAction([
            f"[{self.model}.{self.property}]",
            self.value,
        ])
        action.index = self.index
        action.logical_operator = self.logical_operator
        action.relational_operator = self.relational_operator
        return action
