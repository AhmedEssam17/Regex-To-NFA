from graphviz import *
from collections import defaultdict

# ASCII characters
alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
           [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
           [chr(i) for i in range(ord('0'), ord('9') + 1)] + \
           ['+', ':', ';', '=', '!', '#', '$', '%', '^', '{', '}',
            '[', ']', '/', '!', '&', '-', '_', '^', '~', '<', '>']
# Special characters
leftBracket = '('
rightBracket = ')'
line = '|'
dot = '.'
star = '*'
epsilon = 'ε'


# FA Class
class FiniteAutomata:
    def __init__(self, symbol):
        self.states = set()  # States
        self.symbol = symbol  # Characters
        self.transitions = defaultdict(defaultdict)  # Transitions
        self.startState = None  # Start State
        self.finalStates = []  # List of Final States

    def set_start_state(self, state):  # Start State Function
        self.startState = state  # Add the state to startState variable
        self.states.add(state)  # Add to the set of States created in __init__

    def add_final_state(self, state):  # List of Final States Function
        if isinstance(state, int):
            state = [state]  # Create list of final states
        for s in state:
            if s not in self.finalStates:  # add if not already in the list
                self.finalStates.append(s)

    def add_transition(self, from_state, to_state, input_ch):  # Transitions Function
        if isinstance(input_ch, str):
            input_ch = set([input_ch])  # Create list of input characters
        self.states.add(from_state)  # Add from_states to set of States
        self.states.add(to_state)  # Add to_states to set of States
        if from_state in self.transitions and to_state in self.transitions[from_state]:  # Check transitions in the dict
            self.transitions[from_state][to_state] = self.transitions[from_state][to_state].union(input_ch)
        else:
            self.transitions[from_state][to_state] = input_ch

    def add_transition_dict(self, transitions):  # add transition dictionary to dictionary
        for from_state, to_states in transitions.items():
            for state in to_states:
                self.add_transition(from_state, state, to_states[state])  # Adds transition to dict

    def new_build_from_number(self, start_num):  # Sets the state number (S1, S2, S3,...)
        translations = {}
        for i in self.states:
            translations[i] = start_num  # Store the number of generated states
            start_num += 1
        new_build = FiniteAutomata(self.symbol)
        new_build.set_start_state(translations[self.startState])
        new_build.add_final_state(translations[self.finalStates[0]])
        for from_state, to_states in self.transitions.items():  # Configure transitions according to given states
            for state in to_states:
                new_build.add_transition(translations[from_state], translations[state], to_states[state])
        return [new_build, start_num]

    def get_epsilon_closure(self, find_state):  # Get the set of epsilon transitions for a specific state
        all_states = set()
        states = [find_state]
        while len(states):
            state = states.pop()
            all_states.add(state)
            if state in self.transitions:  # for every state on the same transition
                for to_state in self.transitions[state]:  # Check for epsilon transitions between states
                    if epsilon in self.transitions[state][to_state] and to_state not in all_states:
                        states.append(to_state)
        return all_states

    def get_move(self, state, state_key):  # Check the traversed states for each character states
        if isinstance(state, int):
            state = [state]
        traversed_states = set()  # Create set of traversed states
        for s in state:
            if s in self.transitions:
                for tns in self.transitions[s]:
                    if state_key in self.transitions[s][tns]:
                        traversed_states.add(tns)
        return traversed_states

    def create(self, fname, pname):  # Create image of FA
        automaton = Digraph(pname, filename=fname, format='png')
        automaton.attr(rankdir='LR')

        automaton.attr('node', shape='doublecircle')  # For final states (Double circle states)
        for final_state in self.finalStates:
            automaton.node('s' + str(final_state))

        automaton.attr('node', shape='circle')  # For all other states (Normal circle states)
        for from_state, to_states in self.transitions.items():
            for state in to_states:
                tmp = ''
                for s in to_states[state]:
                    tmp += s + '|'
                automaton.edge('s' + str(from_state), 's' + str(state), label=tmp[:-1])

        automaton.attr('node', shape='point')
        automaton.edge('', 's' + str(self.startState))
        automaton.render(view=False)


class Regex2NFA:

    def __init__(self, regex):  # constructor
        self.regex = regex  # input regular expression
        self.build_nfa()  # builds the NFA

    # create an image of the equivalent NFA of the given regex
    def create_nfa(self):
        self.nfa.create('nfa.gv', 'Non Deterministic Finite Automata')

    @staticmethod
    def get_priority(specialChar):  # Set priority of special characters (dot, OR, star, brackets)
        # Order: Star > Dot > OR > others
        if specialChar == line:    # Lowest
            return 10
        elif specialChar == dot:   # Middle
            return 20
        elif specialChar == star:  # Highest
            return 30
        else:                      # Brackets and Epsilon
            return 0

    @staticmethod
    def simpleCharNFA(oneChar):  # Converts simple Regex to NFA (One character == a)
        state1 = 1  # Set from_state as 1
        state2 = 2  # Set to_state as 2
        simpleNFA = FiniteAutomata({oneChar})  # Generate NFA with the input character
        simpleNFA.set_start_state(state1)  # Set start state
        simpleNFA.add_final_state(state2)  # Set final state/s
        simpleNFA.add_transition(state1, state2, oneChar)  # Generate transitions
        return simpleNFA

    @staticmethod
    def starCharNFA(a):  # Converts star Regex to NFA (One character with star == a*)
        [a, m1] = a.new_build_from_number(2)  # Pass from_state of first char as S2
        state1 = 1  # Set start state as 1
        state2 = m1  # Set final state == to_state of char a
        starNFA = FiniteAutomata(a.symbol)  # Generate NFA with the * of character
        starNFA.set_start_state(state1)  # Set start state as state 1
        starNFA.add_final_state(state2)  # Set final state as state 2
        starNFA.add_transition(starNFA.startState, a.startState, epsilon)  # Generate transitions
        starNFA.add_transition(starNFA.startState, starNFA.finalStates[0], epsilon)
        starNFA.add_transition(a.finalStates[0], starNFA.finalStates[0], epsilon)
        starNFA.add_transition(a.finalStates[0], a.startState, epsilon)
        starNFA.add_transition_dict(a.transitions)  # add transitions dictionary
        return starNFA

    @staticmethod
    def dotCharNFA(a, b):  # Converts star Regex to NFA (One char dot One char == a.b)
        [a, m1] = a.new_build_from_number(1)  # Pass from_state of first char as S1
        [b, m2] = b.new_build_from_number(m1)  # Pass from_state of second char as to_state of first char
        state1 = 1  # Set start state as 1
        state2 = m2 - 1  # Set final state == to_state of char b - 1
        dotNFA = FiniteAutomata(a.symbol.union(b.symbol))  # Generate NFA with the dot of 2 characters
        dotNFA.set_start_state(state1)  # Set start state as state 1
        dotNFA.add_final_state(state2)  # Set final state as state 2
        dotNFA.add_transition(a.finalStates[0], b.startState, epsilon)  # Generate transitions
        dotNFA.add_transition_dict(a.transitions)  # Add transitions dictionary
        dotNFA.add_transition_dict(b.transitions)
        return dotNFA

    @staticmethod
    def orCharNFA(a, b):  # Converts OR Regex to NFA (One char or One char == a|b)
        [a, m1] = a.new_build_from_number(2)  # Pass from_state of first char as S2
        [b, m2] = b.new_build_from_number(m1)  # Pass from_state of second char as to_state of first char
        state1 = 1  # Set start state as 1
        state2 = m2  # Set final state == to_state of char b
        orNFA = FiniteAutomata(a.symbol.union(b.symbol))  # Generate NFA with the OR of 2 characters
        orNFA.set_start_state(state1)  # Set start state as state 1
        orNFA.add_final_state(state2)  # Set final state as state 2
        orNFA.add_transition(orNFA.startState, a.startState, epsilon)  # Generate transitions
        orNFA.add_transition(orNFA.startState, b.startState, epsilon)
        orNFA.add_transition(a.finalStates[0], orNFA.finalStates[0], epsilon)
        orNFA.add_transition(b.finalStates[0], orNFA.finalStates[0], epsilon)
        orNFA.add_transition_dict(a.transitions)  # Add transitions dictionary
        orNFA.add_transition_dict(b.transitions)
        return orNFA

    def build_nfa(self):
        symbol = set()
        prev = ''
        transformed_word = ''

        # Adds dot (.) to regular expressions with more than one operation (Ex: a*(a.b) >> a*.(a.b))
        for ch in self.regex:
            if ch in alphabet:
                symbol.add(ch)
            if ch in alphabet or ch == leftBracket:         # Checks for existence more chars of brackets
                if prev != dot and (prev in alphabet or prev in [star, rightBracket]):
                    transformed_word += dot
            transformed_word += ch
            prev = ch
        self.regex = transformed_word

        # Configure existing priorities and refining the expression to be compatible with the code
        newExpression = ''
        stack = []
        for ch in self.regex:
            if ch in alphabet:
                newExpression += ch
            elif ch == leftBracket:
                stack.append(ch)
            elif ch == rightBracket:
                while stack[-1] != leftBracket:
                    newExpression += stack[-1]
                    stack.pop()
                stack.pop()  # pop left bracket
            else:
                while len(stack) and Regex2NFA.get_priority(stack[-1]) >= Regex2NFA.get_priority(ch):
                    newExpression += stack[-1]
                    stack.pop()
                stack.append(ch)
        while len(stack) > 0:
            newExpression += stack.pop()
        self.regex = newExpression

        # Final step of generating the NFA according to its type
        self.automata = []
        for ch in self.regex:
            if ch in alphabet:                                      # If found char is (a)
                self.automata.append(Regex2NFA.simpleCharNFA(ch))   # simpleChar(a)

            elif ch == line:                                        # If found character are (a|b)
                b = self.automata.pop()                             # orCharNFA(a, b)
                a = self.automata.pop()
                self.automata.append(Regex2NFA.orCharNFA(a, b))

            elif ch == dot:                                         # If found character are (a.b)
                b = self.automata.pop()                             # dotCharNFA(a, b)
                a = self.automata.pop()
                self.automata.append(Regex2NFA.dotCharNFA(a, b))

            elif ch == star:                                        # If found character are (a*)
                a = self.automata.pop()                             # starCharNFA(a)
                self.automata.append(Regex2NFA.starCharNFA(a))
        self.nfa = self.automata.pop()
        self.nfa.symbol = symbol
