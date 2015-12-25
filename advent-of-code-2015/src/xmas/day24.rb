FUDGE = 6 # Speed up brute forcing at the expense of accuracy

presents = [1, 3, 5, 11, 13, 17, 19, 23, 29, 31, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

# prime numbers... thank you santa it's just what I wanted

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


def splits_evenly(group1, presents, weight_target)
    remaining = presents.reject {|present| group1.include?(present)}
    combinations(remaining, weight_target) do |combi|
        if combi == weight_target then
            return true
        end
    end
    false
end

def splits_into_thirds(group1, presents, weight_target)
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
