require_relative 'encode'
require "OpenSSL"
require "set"
require_relative "block"

module ECBDetector
    def self.detect(line)
        seen = Set.new
        line.chars.each_slice(16).each do |block|
            return true if seen.include? block

            seen.add(block)
        end

        false
    end
end

if __FILE__ == $0
    using EncodeHelpers

    decipher = OpenSSL::Cipher.new("aes-128-ecb").decrypt
    ciphertext = IO.read("data/7.txt").gsub("\n", "").decode_base64
    decipher.key = "YELLOW SUBMARINE"
    puts decipher.update(ciphertext) + decipher.final

    puts "---"

    File.foreach("data/8.txt") do |line|
        puts "Detected repeated block: #{line}" if ECBDetector.detect(line.strip.decode_hex)
    end

    100.times do
        # Pass the oracle a long repeating plaintext.
        # If it's using ECB, we can tell from the repeated blocks
        # in the ciphertext.
        method, ciphertext = Block.encryption_oracle("a" * 100)
        puts case [method, ECBDetector.detect(ciphertext)]
        when [:ecb, true]
            :true_positive
        when [:cbc, true]
            :false_positive
        when [:ecb, false]
            :false_negative
        when [:cbc, false]
            :true_negative
        end
    end
end
