sed -E 's/[^-0-9]+/ /g' day12.txt | python -c 'import sys;print sum(int(num) for line in sys.stdin for num in line.split())'
