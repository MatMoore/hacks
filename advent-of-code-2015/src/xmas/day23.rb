class Computer
    def initialize(num_registers=2)
        @num_registers = num_registers
        @registers = Array.new(num_registers, 0)
    end

    def hlf(register_idx)
        @registers[register_idx.to_i] /= 2
        1
    end

    def tpl(register_idx)
        @registers[register_idx.to_i] *= 3
        1
    end

    def inc(register_idx)
        @registers[register_idx.to_i] += 1
        1
    end

    def jmp(offset)
        offset.to_i
    end

    def jie(register_idx, offset)
        if @registers[register_idx.to_i] % 2 == 0 then offset.to_i else 1 end
    end

    def jio(register_idx, offset)
        if @registers[register_idx.to_i] == 1 then offset.to_i else 1 end
    end

    def compute(instructions)
        instruction_idx = 0
        while instruction_idx < instructions.length do
            instruction, *args = instructions[instruction_idx]
            instruction_idx += self.send(instruction, *args)
            #puts(([instruction] + args).to_s)
            #puts(self)
        end
        self
    end

    def to_s
        @registers.to_s
    end
end


def parse_instruction(line)
    tokens = line.split
    tokens[1..-1].map {|t|
        t.delete!('+,')
        t.sub!('a', '0')
        t.sub!('b', '1')
    }
    tokens
end

def parse_instructions(lines)
    lines.map(&method(:parse_instruction))
end

#test = ['inc a',
#        'jio a, +2',
#        'tpl a',
#        'inc a']
#puts(Computer.new(2).compute(parse_instructions(test)))
puts(Computer.new(2).compute([['inc', '0']]).compute(parse_instructions(STDIN)))
