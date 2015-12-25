def neighbours(row, col, size=100)
    [[row, col+1], [row, col-1], [row+1, col], [row-1, col], [row+1, col+1], [row-1, col-1], [row+1, col-1], [row-1, col+1]].
        delete_if {|point| point.any? {|i| i > size || i <= 0}}
end

puts(neighbours(1, 1).to_s)
puts(neighbours(1, 2).to_s)
puts(neighbours(100, 100).to_s)
puts(neighbours(50, 50).to_s)

def count_neighbours(grid, point, size)
    (neighbours(*point, size=size).select {|x|  grid[x]}).length
end

def iterate(grid, size)
    new_grid = grid.map do |point, value|
        if value then
            [point, [2,3].include?(count_neighbours(grid, point, size))]
        else
            [point, count_neighbours(grid, point, size) == 3]
        end
    end.to_h
    new_grid[[1, 1]] = true
    new_grid[[1, size]] = true
    new_grid[[size, size]] = true
    new_grid[[size, 1]] = true
    new_grid
end

def parse(fd)
    grid = {}
    fd.each_with_index do |line, i|
        if line.strip == "" then
            return grid
        end
        line.split("").each_with_index do |c, j|
            if c == '#'
                grid[[i+1, j+1]] = true
            elsif c == '.'
                grid[[i+1, j+1]] = false
            end
        end
    end
    grid
end

def simulate(grid, steps, size)
    grid[[1, 1]] = true
    grid[[1, size]] = true
    grid[[size, size]] = true
    grid[[size, 1]] = true

    for _ in 1..steps
        grid = iterate(grid, size)
    end
    grid
end

def count_lights(grid)
    (grid.values.select{|x| x}).length
end

def display_grid(grid, size)
    (1..size).each do |i|
        line = []
        (1..size).each do |j|
            line.push(if grid[[i, j]] then '#' else '.' end)
        end
        puts(line.join(""))
    end
end

testgrid = parse(['.#.#.#', '...##.', '#....#', '..#...', '#.#..#', '####..'])
#display_grid(testgrid, 6)
#puts("")
testresult = simulate(testgrid, 5, 6)
display_grid(testresult, 6)
puts(count_lights(testresult))

grid = parse(STDIN)
puts(grid.length)
endgrid = simulate(grid, 100, 100)
puts(count_lights(endgrid))
