import re

pattern = re.compile(
    '(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)'
)

lights = {}


def rect(left, top, right, bottom):
    for i in xrange(left, right + 1):
        for j in xrange(top, bottom + 1):
            yield i, j

for line in open('day6.txt'):
    match = pattern.match(line)
    groups = match.groups()
    left = int(groups[1])
    top = int(groups[2])
    right = int(groups[3])
    bottom = int(groups[4])
    for coord in rect(left, top, right, bottom):
        if groups[0] == 'turn on':
            lights[coord] = True
        elif groups[0] == 'turn off':
            lights[coord] = False
        else:
            lights[coord] = not lights.get(coord, False)

print len([1 for item in lights.iteritems() if item[1]])
