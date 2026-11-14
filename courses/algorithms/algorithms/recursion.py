def hanoi(n, source, target, auxiliary):
    if n == 1:
        return [(source, target)]
    steps = hanoi(n-1, source, auxiliary, target)
    steps.append((source, target))
    steps.extend(hanoi(n-1, auxiliary, target, source))
    return steps