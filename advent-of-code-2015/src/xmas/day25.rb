def number_for_indices(row, col)
    if col == 1 and row == 1 then
        return 1
    end

    if col == 1 then
        number_for_indices(row - 1, 1) + row - 1
    else
        number_for_indices(row + col - 1, 1) + col - 1
    end
end

puts(number_for_indices(4, 2) == 12)
puts(number_for_indices(1, 5) == 15)

def generate_nth_code_after(n, code)
    for _ in 1..n
        code = (code * 252533) % 33554393
    end
    code
end

START_CODE = 20151125

puts(generate_nth_code_after(1, START_CODE))
puts(generate_nth_code_after(5, START_CODE))

todays_number = number_for_indices(2981, 3075)
solution = generate_nth_code_after(todays_number - 1, START_CODE)
puts(solution)
