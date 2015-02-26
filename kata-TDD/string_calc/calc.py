import re


HEADER = re.compile('^//(?P<delimiter>[^\n]+)\n(?P<remainder>.*)')


class NegativesNotAllowed(ValueError):
    pass


def validate_numbers(floatlist):
    """
    Validate numbers are positive
    """
    bad = [num for num in floatlist if num < 0]
    if bad:
        raise NegativesNotAllowed(bad)


def parse_header(numbers):
    """
    Parse the optional header and return a tuple of the remainder
    and the delimiter
    """
    match = HEADER.match(numbers)
    if match:
        delimiter = match.group('delimiter')
        remainder = match.group('remainder')
        return remainder, delimiter
    else:
        return numbers, ','


def add(numbers):
    """
    Parse a comma or newline seperated string of numbers and add the results.
    Delimiter may be changed with an optional prefix of the form
    "//[delimiter]\n"
    """
    numbers, delimiter = parse_header(numbers)
    numberlist = numbers.replace('\n', delimiter).split(delimiter)

    # Allow a trailing delimiter
    if not numberlist[-1]:
        numberlist = numberlist[:-1]

    if not numberlist:
        return 0

    floatlist = [float(i) for i in numberlist]

    validate_numbers(floatlist)

    return sum(floatlist)
