
END = "END"

class StateMachine:

    states = {}

    def exist(self, state):
        return state in self.states
    
    def exist_in(self, state_context, state):
        return state in self.states[state_context]
    
    def get_state(self, previous_state, segment):
        raise NotImplementedError()

    def pre_process(self, grouped_actions):
        pass

    def post_process(self, grouped_actions):
        pass

from qapi.state_machine.querystring import QuerystringStateMachine