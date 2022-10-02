import string, random

def generate_random_string(n: int = 5) -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))