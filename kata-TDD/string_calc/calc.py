import re
SEP = re.compile('[,\n]')
HEADER = re.compile('^//(?P<delimiter>[^\n]+)\n(?P<remainder>.*)')


def add(numbers):
    if not numbers:
        return 0

    match = HEADER.match(numbers)
    if match:
        delimiter = re.escape(match.group('delimiter'))
        delimiter_regex = re.compile('(?:\n)|(?:{})'.format(delimiter))
        numbers = match.group('remainder')
    else:
        delimiter_regex = SEP

    numberlist = delimiter_regex.split(numbers)
    return sum(float(i) for i in numberlist)
