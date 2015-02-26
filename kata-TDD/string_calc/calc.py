import re
SEP = re.compile('[,\n]')


def add(numbers):
    if not numbers:
        return 0

    numberlist = SEP.split(numbers)
    return sum(float(i) for i in numberlist)
