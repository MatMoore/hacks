import math
import pytest
from calc import add, NegativesNotAllowed


def test_add_empty_is_zero():
    """
    For an empty string, add returns 0
    """
    assert add('') == 0


def test_none_is_zero():
    """
    None is a typeerror
    """
    with pytest.raises(TypeError):
        add(None)


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
    Negatives aren't allowed
    """
    with pytest.raises(NegativesNotAllowed):
        add('1,-2')


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


def test_five_numbers():
    """
    Should be able to add any number of numbers
    """
    assert add('1,2,3,4,5') == 15


def test_newlines_commas_interchangable():
    """
    Newlines can be used in place of commas
    """
    assert add('1\n2\n3') == 6


def test_repeated_same_seperators_invalid():
    """
    Multiple seperators of the same type are invalid
    """
    with pytest.raises(ValueError):
        add('1,,2')


def test_repeated_diff_seperators_invalid():
    """
    Multiple seperators of different type are invalid
    """
    with pytest.raises(ValueError):
        add('1,\n2')


def test_delimiter_change_valid_use():
    """
    First line can change the delimeter
    """
    assert add('//*\n1*2') == 3


def test_delimiter_change_invalid_use():
    """
    If the delimiter is changed, comma is no longer valid
    """
    with pytest.raises(ValueError):
        add('//*\n1,2')


def test_trailing_delimiter():
    """
    Trailing delimiters are ignored
    """
    assert add('//|\n1|2|') == 3


def test_only_trailing_delimiter():
    """
    Delimiter with no numbers is invalid
    """
    with pytest.raises(ValueError):
        add(',')


def test_only_header():
    """
    Header with no numbers should be zero
    """
    assert add('//&\n') == 0


def test_header_missing_newline():
    """
    Header must be followed by a newline
    """
    with pytest.raises(ValueError):
        add('//&1,2,3')
