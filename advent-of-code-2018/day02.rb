require 'set'

double_letter_count = 0
triple_letter_count = 0
boxids = []

# All variations of a box id produced by removing one of its letters
def variations(boxid)
    result = []
    0.upto(boxid.length - 1) do |offset|
        next_offset = offset + 1

        # Append the offset of the letter we removed, because when matching the codes
        # the letter has to be removed from the same position
        result << (boxid[0...offset] + boxid[next_offset...boxid.length] + "[#{offset}]")
    end

    return result
end

File.open('inputs/day02.txt') do |f|
    f.each_line do |line|
        lengths = line.chars.sort.group_by(&:itself).map {|k,v| v.length}.to_set

        if lengths.include?(2)
            double_letter_count += 1
        end
        if lengths.include?(3)
            triple_letter_count += 1
        end

        variations(line.strip).each do |variation|
            boxids << variation
        end
    end
end

# Part 1
puts double_letter_count * triple_letter_count

# Part 2
puts boxids.sort.group_by(&:itself).select {|k, v| v.length == 2}.first.first