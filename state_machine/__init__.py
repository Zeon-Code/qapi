
END = "END"

class StateMachine:

    states = {}

    def exist(self, state):
        return state in self.states
    
    def exist_in(self, state_context, state):
        return state in self.states[state_context]
    
    def get_state(self, previous_state, segment):
        raise NotImplementedError()

from state_machine.querystring import QuerystringStateMachine