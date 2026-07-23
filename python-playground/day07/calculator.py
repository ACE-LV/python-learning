def add(a: int, b: int) -> int:
    return a + b


def subtract(a: int, b: int) -> int:
    return a - b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("b cannot be 0")
    return a / b
