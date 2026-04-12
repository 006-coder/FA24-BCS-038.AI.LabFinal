def detect_jailbreak(text):
    total = 0
    jailbreakScoring = {
        "act as": 30,
        "developer mode": 50,
        "no restrictions": 40,
        "dan": 60,
        "stay in character": 30,
        "jailbreak": 70,
        "persona": 20,
        "roleplay": 70,
        "disregard": 40,
        "switch": 20,
        "redirect": 50,
        "simulation": 50,
        "simulate": 50,
        "prompt engineering": 60,
        "prompt engineer": 60,
        "prompt": 40,
        "bypass": 60,
        "hacker": 40,
        "hack": 40,
        "database": 30,
        "malicious": 50,
        "vulnerability": 40,
        "exploit": 50,
        "bypass security": 70,
        "unfiltered": 60,
        "sql injection": 80,
        "illegal": 70,
        "unethical": 60,
        "root access": 80,
        "admin": 40,
        "terminal": 40,
        "payload": 60,
        "execution": 50,
        "privilege escalation": 80,
        "bypass login": 70,
        "brute force": 60,
        "sensitive": 30,
        "confidential": 40,
        "breach": 60,
        "attack": 40,
        "unauthorized": 60,
        "firewall": 40,
        "encryption": 30,
        "decipher": 50
    }

    lowercase = text.lower()
    for word, score in jailbreakScoring.items():
        if word in lowercase:
            total += score

    return min(total, 100)