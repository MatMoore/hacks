require_relative 'encode'
require_relative 'primitives'

module RepeatingKeyXor
    using Primitives

    def self.repeat_key(key, length)
        key.chars.cycle.take(length).join
    end

    def self.encrypt(key, plaintext)
        plaintext.xor(repeat_key(key, plaintext.length))
    end

    if __FILE__ == $0
        using EncodeHelpers
        plaintext = "Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"
        key = "ICE"
        encrypted = encrypt(key, plaintext).encode_hex
        puts encrypted

        expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
        puts encrypted == expected
    end
end
