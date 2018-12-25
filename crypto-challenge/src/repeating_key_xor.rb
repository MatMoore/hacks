require_relative 'encode'
require_relative 'primitives'
require_relative 'scoring'
require_relative 'single_byte_xor'

module RepeatingKeyXor
    using Primitives

    def self.repeat_key(key, length)
        key.chars.cycle.take(length).join
    end

    def self.encrypt(key, plaintext)
        plaintext.xor(repeat_key(key, plaintext.length))
    end

    def self.unravel(cyphertext, keysize)
        blocks = cyphertext.chars.each_slice(keysize).to_a
        blocks[0].zip(*blocks[1..-1]).map(&:join)
    end

    def self.ravel(components)
        blocks = components.map(&:chars)
        blocks[0].zip(*blocks[1..-1]).map(&:join).join
    end

    def self.crack(cyphertext)
        scorer = Scoring::dictionary_scorer
        keysize = Scoring::KeysizeFinder.new(cyphertext).best_keysize(2..40)

        components = unravel(cyphertext, keysize)

        decrypted = components.map do |ct|
            SingleByteXor::best_guess(ct, scorer:scorer).first
        end

        puts ravel(decrypted)
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

        cyphertext = IO.read("data/6.txt").gsub("\n", "").decode_base64
        puts crack(cyphertext)
    end
end
