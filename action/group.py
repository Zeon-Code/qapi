from collections import defaultdict


class ActionGroup:

    @property
    def actions(self):
        return dict(self._actions)

    def __init__(self):
        self._actions = defaultdict(dict)
        self.total = 0

    def add(self, action):
        context = self._get_context(action)
        context.append(action)
        self.total += 1

    def delete(self, action):
        context = self._get_context(action)
        context.remove(action)
        self._delete_context(action)
        self.total -= 1

    def _get_context(self, action):
        if action.context not in self._actions[action.type]:
            self._actions[action.type][action.context] = []
        return self._actions[action.type][action.context]

    def _delete_context(self, action):
        if not self._actions[action.type][action.context]:
            del self._actions[action.type][action.context]
        
        if not self._actions[action.type]:
            del self._actions[action.type]
