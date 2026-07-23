from calculator import add, divide, subtract


def test_add() -> None:
    assert add(1, 2) == 3


def test_subtract() -> None:
    assert subtract(5, 3) == 2


def test_divide() -> None:
    assert divide(10, 2) == 5


def test_divide_by_zero() -> None:
    try:
        divide(10, 0)
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "b cannot be 0"
