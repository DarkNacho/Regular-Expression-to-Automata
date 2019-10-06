from ER import ER_to_NFA

nfa = ER_to_NFA("a.b")
nfa.evaluate("aaabababbbbb")
print nfa
