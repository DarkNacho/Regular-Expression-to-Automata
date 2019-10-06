class _Transition:
    def __init__(self, key='_', v1=0, v2=0):
        self.key = key
        self.state_from = v1
        self.state_to = v2


class NFA:
    def __init__(self, value):
        self.matches = []
        self.terminal = 0
        self.states = []
        self.transitions = []
        if isinstance(value, int):
            self.setStateSize(value)
        else:
            self.setStateSize(2)
            self.terminal = 1
            if value[-1] == '*':
                temp = NFA(value[0]).kleene()
                self.terminal = temp.terminal
                self.states = temp.states
                self.transitions = temp.transitions
            else:
                self.transitions.append(_Transition(value, 0, 1))

    def getAdjacenceList(self):
        list = [[] for j in range(len(self.transitions))]
        for t in self.transitions:
            list[t.state_from].append(t.state_to)
        return list

    def setStateSize(self, n):
        self.states = [i for i in range(n)]

    def concat(self, nfa):
        nfa.states.pop(0)
        for t in nfa.transitions:
            self.transitions.append(
                _Transition(t.key, t.state_from + len(self.states) - 1, t.state_to + len(self.states) - 1))

        for s in nfa.states:
            self.states.append(s + len(self.states) + 1)

        self.terminal = len(self.states) + len(nfa.states) - 2
        return self

    def union(self, nfa):
        result = NFA(len(self.states) + len(nfa.states) + 2)
        result.transitions.append(_Transition("_", 0, 1))
        for t in self.transitions:
            result.transitions.append((_Transition(t.key, t.state_from + 1, t.state_to + 1)))

        result.transitions.append(_Transition("_", len(self.states), len(self.states) + len(nfa.states) + 1))

        result.transitions.append(_Transition("_", 0, len(self.states) + 1))

        for t in nfa.transitions:
            result.transitions.append(
                (_Transition(t.key, t.state_from + len(self.states) + 1, t.state_to + len(self.states) + 1)))

        result.transitions.append(
            _Transition("_", len(nfa.states) + len(self.states), len(nfa.states) + len(self.states) + 1))

        result.terminal = len(self.states) + len(nfa.states) + 1
        self = result
        return self;

    def kleene(self):
        result = NFA(len(self.states) + 2)
        result.transitions.append(_Transition("_", 0, 1))

        for t in self.transitions:
            result.transitions.append(_Transition(t.key, t.state_from + 1, t.state_to + 1))

        result.transitions.append(_Transition("_", len(self.states), len(self.states) + 1))
        result.transitions.append(_Transition("_", len(self.states), 1))
        result.transitions.append(_Transition("_", 0, len(self.states) + 1))

        result.terminal = len(self.states) + 1
        self = result
        return self

    def __dfs(self, node, regex, index, adj):
        if self.terminal == node:
            self.matches.append(len(regex) - 1 - index)
        if index >= 0 and node < len(self.transitions):
            key = regex[index]
            for u in adj[node]:
                if u != self.terminal:
                    if self.transitions[u] == "_":
                        self.__dfs(u, regex, index - 1, adj)
                if self.transitions[node].key == key:
                    self.__dfs(u, regex, index - 1, adj)
        return index

    def evaluate(self, regex):
        adjlist = self.getAdjacenceList()
        regex = list(regex)
        regex.reverse()
        index = len(regex)
        while index >= 0:
            index = self.__dfs(0, regex, index - 1, adjlist)

    def __str__(self):
        k = "q".join([str(i) + "," for i in range(len(self.states))])
        k = "K={q" + k[:-1] + "}\n"
        delta = "delta:\n"
        sigma = set()
        for t in self.transitions:
            sigma.add(t.key)
            delta += "(q" + str(t.state_from) + "," + str(t.key) + ",q" + str(t.state_to) + ")\n"
        sigma = "Sigma={" + ",".join(sorted(sigma)) + "}\n"

        match = "\nOcurrencias:\n"
        for i in self.matches:
            match += str(i) + " "

        return "AFD:\n" + k + sigma + delta + "s=q0\n" + "F={q" + str(self.terminal) + "}\n" + match
