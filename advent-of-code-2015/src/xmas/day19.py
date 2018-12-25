import string
from collections import defaultdict, deque
import random

rules = [
    'Al => ThF',
    'Al => ThRnFAr',
    'B => BCa',
    'B => TiB',
    'B => TiRnFAr',
    'Ca => CaCa',
    'Ca => PB',
    'Ca => PRnFAr',
    'Ca => SiRnFYFAr',
    'Ca => SiRnMgAr',
    'Ca => SiTh',
    'F => CaF',
    'F => PMg',
    'F => SiAl',
    'H => CRnAlAr',
    'H => CRnFYFYFAr',
    'H => CRnFYMgAr',
    'H => CRnMgYFAr',
    'H => HCa',
    'H => NRnFYFAr',
    'H => NRnMgAr',
    'H => NTh',
    'H => OB',
    'H => ORnFAr',
    'Mg => BF',
    'Mg => TiMg',
    'N => CRnFAr',
    'N => HSi',
    'O => CRnFYFAr',
    'O => CRnMgAr',
    'O => HP',
    'O => NRnFAr',
    'O => OTi',
    'P => CaP',
    'P => PTi',
    'P => SiRnFAr',
    'Si => CaSi',
    'Th => ThCa',
    'Ti => BP',
    'Ti => TiTi',
    'e => HF',
    'e => NAl',
    'e => OMg',
]

rules_dict = defaultdict(set)
inverted_dict = {}
for start, end in [item.split(' => ') for item in rules]:
    rules_dict[start].add(end)
    inverted_dict[end] = start


molecule = 'ORnPBPMgArCaCaCaSiThCaCaSiThCaCaPBSiRnFArRnFArCaCaSiThCaCaSiThCaCaCaCaCaCaSiRnFYFArSiRnMgArCaSiRnPTiTiBFYPBFArSiRnCaSiRnTiRnFArSiAlArPTiBPTiRnCaSiAlArCaPTiTiBPMgYFArPTiRnFArSiRnCaCaFArRnCaFArCaSiRnSiRnMgArFYCaSiRnMgArCaCaSiThPRnFArPBCaSiRnMgArCaCaSiThCaSiRnTiMgArFArSiThSiThCaCaSiRnMgArCaCaSiRnFArTiBPTiRnCaSiAlArCaPTiRnFArPBPBCaCaSiThCaPBSiThPRnFArSiThCaSiThCaSiThCaPTiBSiRnFYFArCaCaPRnFArPBCaCaPBSiRnTiRnFArCaPRnFArSiRnCaCaCaSiThCaRnCaFArYCaSiRnFArBCaCaCaSiThFArPBFArCaSiRnFArRnCaCaCaFArSiRnFArTiRnPMgArF'


def findall(needle, haystack):
    """
    Find all occurences of a substring, with overlaps
    """
    result = []
    idx = 0
    while True:
        idx = haystack.find(needle, idx)
        if idx == -1:
            break
        result.append(idx)
        idx = idx + 1
    return result


def possible_transformations(rules_dict, molecule):
    possible_molecules = set()
    for candidate, transformations in rules_dict.iteritems():
        found_candidates = findall(candidate, molecule)
        for found_candidate in found_candidates:
            for transformation in transformations:
                possible_molecule = (
                    molecule[:found_candidate] +
                    transformation +
                    molecule[found_candidate + len(candidate):]
                )
                possible_molecules.add(possible_molecule)

    return possible_molecules


def possible_reverse_transformations(rules, current_state):
    result = set()
    for start, end in rules:
        for idx in findall(start, current_state):
            origin = current_state[:idx] + end + current_state[idx + len(start):]
            result.add(origin)
    return result


def find_steps(target, rules_dict, start='e'):
    """
    Breadth first search for a series of transformations that leads to
    the target molecule
    """
    current_paths = deque([[start]])
    while True:
        current_path = current_paths.popleft()
        current_state = current_path[-1]
        for new_state in possible_transformations(rules_dict, current_state):
            new_path = current_path[:]
            new_path.append(new_state)
            if new_state == target:
                return new_path
            if len(new_state) > len(target):
                # No transformation makes the string shorter, so we can give up here
                continue
            current_paths.append(new_path)


def find_steps_backwards(start, rules_dict, target='e'):
    """
    Same as above but the opposite way round
    """
    current_paths = deque([[start]])
    rules = sorted(rules_dict.items(), key=lambda x: len(x[0]) - len(x[1]), reverse=True)
    while True:
        current_path = current_paths.popleft()
        current_state = current_path[-1]
        for new_state in possible_reverse_transformations(rules, current_state):
            new_path = current_path[:]
            new_path.append(new_state)
            if new_state == target:
                return new_path
            current_paths.append(new_path)


def greedy_simplify(start, rules_dict, target='e'):
    """
    Trying to apply the longest simplification each time.
    It didn't work
    """
    if start == target:
        return 0

    rules = rules_dict.items()
    random.shuffle(rules)
    rules = sorted(rules, key=lambda x: len(x[0]), reverse=True)

    for a, b in rules:
        for idx in findall(a, start):
            new_start = start[:idx] + b + start[idx + len(a):]
            remainder = greedy_simplify(new_start, rules_dict, target)
            if remainder is not None:
                return remainder + 1

    return None


def count_molecule(molecule):
    """
    https://www.reddit.com/r/adventofcode/comments/3xflz8/day_19_solutions/cy4etju
    """
    molecule = molecule.replace('Rn', '(')
    molecule = molecule.replace('Ar', ')')
    molecule = molecule.replace('Y', ',')
    uppercase = sum(1 for i in molecule if i in string.uppercase)
    comma = sum(1 for i in molecule if i == ',')
    total = uppercase - comma - 1
    return total


if __name__ == '__main__':
    test_dict = {'H': {'HO', 'OH'}, 'O': {'OH'}}
    test_dict2 = {'e': {'H', 'O'}, 'H': {'HO', 'OH'}, 'O': {'HH'}}
    test_dict2i = {'H': 'e', 'O': 'e', 'HO': 'H', 'OH': 'H', 'HH': 'O'}
    test_molecule = 'HOHOHO'
    print len(possible_transformations(rules_dict, molecule))
    #print find_steps('HOHOHO', test_dict2)
    #print find_steps_backwards('HOHOHO', test_dict2i)
    #print greedy_simplify('HOHOHO', test_dict2i)
    print count_molecule(molecule)
