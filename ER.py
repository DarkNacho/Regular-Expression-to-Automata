from Parser import postfix_parse
from NFA import NFA


def ER_to_NFA(ER):
    stack = []
    ER = postfix_parse(ER)
    tokens = []
    for t in ER:
        tokens.append(NFA(t) if t not in "|." else t)

    if len(tokens) == 1:
        return tokens.pop()

    for token in tokens:
        result = None
        if isinstance(token, NFA):
            stack.append(token)
        else:
            op2 = stack.pop()
            op1 = stack.pop()
            result = (op1.concat(op2) if token == '.' else op1.union(op2))
            stack.append(result)
    return stack.pop()
