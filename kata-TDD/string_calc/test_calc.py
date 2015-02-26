from calc import add
import math


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


def test_two_int():
    """
    Two numbers are added together
    """
    result = add('1,2')
    assert result == 3
    assert isinstance(result, float)


def test_negative_numbers():
    """
    Positive and negative numbers are added together
    """
    result = add('1,-2')
    assert result == -1
    assert isinstance(result, float)


def test_floating_numbers():
    """
    Floating point numbers are added together
    """
    result = add('1.1,1.2')
    assert result == 2.3
    assert isinstance(result, float)


def test_scientific_numbers():
    """
    Scientific notation numbers are added together
    """
    result = add('1e-6,1e2')
    assert result == 100.000001
    assert isinstance(result, float)


def test_add_infinities():
    """
    Adding infinities gives more infinity
    """
    result = add('inf,2')
    assert result == float('inf')
    assert isinstance(result, float)


def test_add_negative_zero():
    """
    Zeroes can be negative too
    """
    result = add('1,-0')
    assert result == 1
    assert isinstance(result, float)


def test_add_nan():
    """
    NaN breaks the computation
    """
    result = add('NaN,1')
    assert math.isnan(result)
    assert isinstance(result, float)
