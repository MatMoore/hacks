from calc import add


def test_add_empty_is_zero():
    """
    For an empty string, add returns 0
    """
    assert add('') == 0
