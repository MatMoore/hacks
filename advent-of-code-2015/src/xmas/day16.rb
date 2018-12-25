analysis = {
    'children' => 3,
    'cats' => 7,
    'samoyeds' => 2,
    'pomeranians' => 3,
    'akitas' => 0,
    'vizslas' => 0,
    'goldfish' => 5,
    'trees' => 3,
    'cars' => 2,
    'perfumes' => 1,
}

def matches(remembered, analysis)
    remembered.all? do |k, number|
        if ['cats', 'trees'].include?(k) then
            analysis[k].nil? || analysis[k] < number
        elsif ['pomeranians', 'goldfish'].include?(k) then
            analysis[k].nil? || analysis[k] > number
        else
            analysis[k].nil? || analysis[k] == number
        end
    end
end

def parse(line)
    parts = line.sub('Sue ', '').split(/[,:] /)
    sue = parts[0]
    facts = parts[1..-1].each_slice(2)
    facts = facts.map {|k, v| [k, v.to_i]}.to_h
    [sue, facts]
end

#puts(parse("Sue 1: cars: 9, akitas: 3, goldfish: 0").to_s)
#puts(matches(analysis, analysis))
#puts(matches({}, analysis))
#puts(matches({'cats': 7, 'children': 3}, analysis))
#puts(matches({'cats': 8, 'children': 3}, analysis))

sues = STDIN.map {|line| parse(line)}
puts(sues.select {|sue, facts| matches(facts, analysis)})
