presents = [1, 3, 5, 11, 13, 17, 19, 23, 29, 31, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

# Prime numbers... why thank you Santa, it's just what I always wanted...

total_weight = presents.reduce(:+)
weight_target = total_weight / 3
weight_target2 = total_weight / 4

group1_candidates = presents.combination(6).select {|c| c.reduce(:+) == weight_target}.sort_by {|group1| group1.reduce(:*)}
group1_candidates2 = presents.combination(5).select {|c| c.reduce(:+) == weight_target2}.sort_by {|group1| group1.reduce(:*)}

# Enumerates all possible selections for the second group,
# while skipping any that exceed the weight target
# Returns the sum of the selections.
def combinations(arr, weight_target)
    if(arr.empty?) then
        yield 0
    else
        combinations(arr[1..-1], weight_target) do |combi|
            with = arr[0] + combi
            without = combi
            yield without
            if with <= weight_target then
                yield with
            end
        end
    end
end

# Very inelegent extension of the idea from part 1...
# There are now 3^N possible groupings instead of 2^N
def combinations2(arr, weight_target)
    if(arr.empty?) then
        yield [0, 0]
    else
        combinations2(arr[1..-1], weight_target) do |group2, group3|
            add_to_group2 = arr[0] + group2
            add_to_group3 = arr[0] + group3
            without = [group2, group3]

            # Randomising here means it can converge on a solution faster if there is one (luckily there is)
            # otherwise we are biased towards towards unevenly distributed solutions, which are less likely to meet our criteria
            possibilities = [without]
            if add_to_group2 <= weight_target then
                possibilities.push([add_to_group2, group3])
            end
            if add_to_group3 <= weight_target then
                possibilities.push([group2, add_to_group3])
            end
            possibilities.shuffle.each {|x| yield x}
        end
    end
end

def splits_evenly(group1, presents, weight_target)
    remaining = presents.reject {|present| group1.include?(present)}
    combinations(remaining, weight_target) do |combi|
        if combi == weight_target then
            return true
        end
    end
    false
end

# More clunky rewriting of part 1, yay
def splits_into_thirds(group1, presents, weight_target)
    remaining = presents.reject {|present| group1.include?(present)}
    puts(remaining.length)
    combinations2(remaining, weight_target) do |combi|
        if combi.all? {|group| group == weight_target} then
            return true
        end
    end
    false
end


puts("Narrowed to #{group1_candidates.length} candidates")
group1_candidates.each do |group1|
    if splits_evenly(group1, presents, weight_target)
        puts(group1.to_s)
        puts(group1.reduce(:*))
        break
    else
        puts("Rejected #{group1}")
    end
end

puts("Narrowed to #{group1_candidates2.length} candidates")
group1_candidates2.each do |group1|
    if splits_into_thirds(group1, presents, weight_target2)
        puts(group1.to_s)
        puts(group1.reduce(:*))
        break
    else
        puts("Rejected #{group1}")
    end
end
