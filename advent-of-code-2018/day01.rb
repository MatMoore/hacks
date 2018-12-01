require 'set'

observed_frequencies = Set.new
current_frequency = 0
while true
    File.open('inputs/day01.txt') do |f|
        f.each_line do |line|
            current_frequency += line.to_i
            if observed_frequencies.include?(current_frequency)
                puts "frequency observed twice: #{current_frequency}"
                exit
            end
            observed_frequencies.add(current_frequency)
        end
    end
end

#puts "final frequency: #{current_frequency}"