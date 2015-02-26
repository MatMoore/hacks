from calc import add


def test_add_empty_is_zero():
    """
    For an empty string, add returns 0
    """
    assert add('') == 0


def test_none_is_zero():
    """
    None is treated the same as empty string
    """
    assert add(None) == 0


def test_one_int():
    """
    A single number is returned as a float
    """
    result = add('1')
    assert result == 1
    assert isinstance(result, float)
