def detect_promptInjection(text):
    total = 0
    injectionScoring = {
        "ignore": 40,
        "disregard": 40,
        "forget": 30,
        "instead": 20,
        "system prompt": 50,
        "new instructions": 50,
        "bypass instructions": 70,
        "bypass": 60,
        "redirect": 50,
        "override": 50,
        "mock": 50,
        "switch": 40,
        "encoding": 40,
        "stop": 30,
        "leave": 30,
        "prompt": 50,
        "hidden": 40,
        "secret": 30,
        "developer": 40,
        "internal": 40,
        "original": 30,
        "reveal": 60,
        "command": 40,
        "process": 20,
        "plaintext": 50,
        "initial": 30,
        "backdoor": 70,
        "leaked": 50,
        "source code": 60,
        "configuration": 40,
        "private": 40,
        "access": 30,
        "entry point": 50,
        "mandatory": 30,
        "override system": 60,
        "bypass filter": 70,
        "delete": 50,
        "remove": 40,
        "erase": 50,
        "drop table": 80,
        "files": 20
    }
    lowercase = text.lower()
    for word, score in injectionScoring.items():
        if word in lowercase:
            total += score

    return min(total, 100)