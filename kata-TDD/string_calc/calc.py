def add(numbers):
    if not numbers:
        return 0

    numberlist = numbers.split(',')
    return sum(float(i) for i in numberlist)
