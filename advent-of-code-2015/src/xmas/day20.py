PRESENTS_PER_HOUSE = 11
HOUSE_LIMIT = 50


def distribute_presents(limit):
    result = [0 for i in xrange(limit)]
    for i in xrange(1, limit):
        for j in xrange(i, i * HOUSE_LIMIT + 1, i):
            if j >= limit:
                break
            result[j] += i
    return result


if __name__ == '__main__':
    target = 33100000
    presents = distribute_presents(target / PRESENTS_PER_HOUSE)
    for i in xrange(1, target / PRESENTS_PER_HOUSE):
        if presents[i] * PRESENTS_PER_HOUSE >= target:
            print i
            break
