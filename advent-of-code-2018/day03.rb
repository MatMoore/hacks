Command = Struct.new(:elf, :x, :y, :width, :height)
Point = Struct.new(:x, :y)

def parse_line(line)
    match = /^\#(?<elf>\d+)\s    @\s(?<x>\d+),(?<y>\d+):    \s(?<width>\d+)x(?<height>\d+)$/x.match(line.strip)
    return Command.new(match[:elf].to_i, match[:x].to_i, match[:y].to_i, match[:width].to_i, match[:height].to_i)
end

commands = IO.foreach('inputs/day03.txt').map { |x| parse_line(x) }
fabric = Hash.new { |hash, key| hash[key] = [] }

non_overlapping = Set.new

commands.each do |command|
    non_overlapping.add(command.elf)

    command.x.upto(command.x + command.width - 1) do |i|
        command.y.upto(command.y + command.height - 1) do |j|
            p = Point.new(i, j)
            fabric[p] << command.elf

            if fabric[p].length > 1
                fabric[p].each do |elf|
                    non_overlapping.delete(elf)
                end
            end
        end
    end
end

def render(fabric, width, height)
    0.upto(width - 1) do |x|
        0.upto(height - 1) do |y|
            print fabric[Point.new(x,y)].length
        end
        puts ""
    end
end

puts fabric.values.select { |elves| elves.length > 1 }.count
puts non_overlapping
