require_relative 'encode'

module Primitives
    using EncodeHelpers
    refine String do
        def xor(another)
            bytes.zip(another.bytes).map {|pair| pair.first ^ pair.last}
                .pack('c*')
        end

        def hamming_distance(another)
            sum = 0

            bytes.zip(another.bytes).each do |pair|
                byte = pair.first ^ pair.last
                while byte != 0
                    sum += byte & 1
                    byte = byte >> 1
                end
            end

            sum
        end

        def pad_to_size(blocksize)
            padding_size = (blocksize - size)
            self + [padding_size].pack('C') * padding_size
        end
    end
end


if __FILE__ == $0
    using Primitives
    using EncodeHelpers
    hex1 = '1c0111001f010100061a024b53535009181c'
    hex2 = '686974207468652062756c6c277320657965'
    expected = '746865206b696420646f6e277420706c6179'
    actual = hex1.decode_hex.xor(hex2.decode_hex).encode_hex
    puts actual
    puts actual == expected

    puts 'this is a test'.hamming_distance('wokka wokka!!!') == 37

    padded = "YELLOW SUBMARINE".pad_to_size(20)
    puts padded.encode_hex
    puts padded == "YELLOW SUBMARINE\x04\x04\x04\x04"
end
