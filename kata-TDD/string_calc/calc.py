import re
SEP = re.compile('[,\n]')
HEADER = re.compile('^//(?P<delimiter>[^\n]+)\n(?P<remainder>.*)')


class NegativesNotAllowed(ValueError):
    pass


def validate_numbers(floatlist):
    bad = [num for num in floatlist if num < 0]
    if bad:
        raise NegativesNotAllowed(bad)


def add(numbers):
    match = HEADER.match(numbers)
    if match:
        delimiter = re.escape(match.group('delimiter'))
        delimiter_regex = re.compile('(?:\n)|(?:{})'.format(delimiter))
        numbers = match.group('remainder')
    else:
        delimiter = ','
        delimiter_regex = SEP

    numberlist = delimiter_regex.split(numbers)

    # Allow a trailing delimiter
    if not numberlist[-1]:
        numberlist = numberlist[:-1]

    if not numberlist:
        return 0

    floatlist = [float(i) for i in numberlist]

    validate_numbers(floatlist)

    return sum(floatlist)
