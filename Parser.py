def __parse(text):
    out = []
    for c in text:
        if c != '*':
            out.append(c)
        else:
            out[-1] += c
    return out


def postfix_parse(ER):
    precedence = {".": 2, "|": 1}
    stack = []
    postfix = []
    tokens = __parse(ER)
    for token in tokens:
        if token not in "*.|":
            postfix.append(token)
        else:
            while len(stack) and (precedence[stack[-1]] >= precedence[token]):
                postfix.append(stack.pop())
            stack.append(token)
    while len(stack):
        postfix.append(stack.pop())
    return postfix
    # return "".join(suffix)
