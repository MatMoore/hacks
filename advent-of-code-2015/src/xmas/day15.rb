INGREDIENTS = {
    :sprinkles => {:capacity => 2, :durability => 0, :flavor => -2, :texture => 0, :calories => 3},
    :butterscotch => {:capacity => 0, :durability => 5, :flavor => -3, :texture => 0, :calories => 3},
    :chocolate => {:capacity => 0, :durability => 0, :flavor => 5, :texture => -1, :calories => 8},
    :candy => {:capacity => 0, :durability => -1, :flavor => 0, :texture => 5, :calories => 8}
}

TEST_INGREDIENTS = {
    :butterscotch => {:capacity => -1, :durability => -2, :flavor => 6, :texture => 3, :calories => 8},
    :cinnamon => {:capacity => 2, :durability => 3, :flavor => -2, :texture => -1, :calories => 3}
}

# Score a mix
def score(mix, ingredients)
    [:capacity, :durability, :flavor, :texture].map do |property|
        mix.map {|ingredient, quantity| quantity * ingredients[ingredient][property]}.reduce(:+)
    end.reduce(1) {|result, total| result * [0, total].max}
end

# Count the calories for a mix
def calory_count(mix, ingredients)
    mix.reduce(0) do |total, (ingredient, quantity)|
        total + ingredients[ingredient][:calories] * quantity
    end
end

# Brute force search for generating mixes of ingredients
def find_mixes(ingredients, n)
    num_partitions = ingredients.length - 1
    Enumerator.new do |y|
        # Ick.. this is rubbish, but it works
        # We get multiple copies of the same partitioning here.
        ranges = [(0..n).to_a] * num_partitions
        partitionings = ranges[0].product(*ranges[1..-1]).map {|x| x.sort}

        # Here we just look at the possible ways of partitioning the number line
        # into the right number of groups (groups can be zero-sized).
        partitionings.each do |partitions|
            result = {}
            partitions = partitions.unshift(0)
            indices = partitions.zip(partitions[1..-1], ingredients)
            indices.each do |first, partition, ingredient|
                result[ingredient] = (partition || n) - first
            end
            y << result
        end
    end
end

# Same as above but with calory restriction
def find_mixes_with_calories(ingredients, n, num_calories=500)
    find_mixes(ingredients.keys, n).select {|mix| calory_count(mix, ingredients) == num_calories}
end

#puts(score({:butterscotch => 44, :cinnamon => 56}, TEST_INGREDIENTS))
#find_mixes(TEST_INGREDIENTS.keys, 100).each {|x| puts(x.to_s)}
#puts(score({:sprinkles=>98, :butterscotch=>1, :chocolate=>1, :candy=>0}, INGREDIENTS))
#puts(find_mixes(TEST_INGREDIENTS.keys, 100).max_by {|mix| score(mix, TEST_INGREDIENTS)})
best = find_mixes_with_calories(INGREDIENTS, 100).max_by {|mix| score(mix, INGREDIENTS)}
best_score = score(best, INGREDIENTS)
puts(best)
puts(best_score)
