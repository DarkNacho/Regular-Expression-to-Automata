def postfix_parse(ER):
    precedence = {"*":3, ".": 2, "|": 1}
    stack = []
    postfix = []
    tokens = list(ER) 
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
