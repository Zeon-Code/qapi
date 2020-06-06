from action import Action


class OrderAction(Action):

    type = "order"

    @property
    def context(self):
        return self.index

    def __init__(self, segments):
        self.index = self._parse_index(segments[0])
        constraint, self.value = segments[1].split(" ")
        self.model, self.property = self._parse_constraint(constraint)

    def copy(self):
        return OrderAction([
            f"[{self.index}]",
            f"{self.model}.{self.property} {self.value}",
        ])
