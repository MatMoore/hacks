require_relative 'encode'
require "OpenSSL"
require "set"

module AESDetector
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
    ciphertext = IO.read("7.txt").gsub("\n", "").decode_base64
    decipher.key = "YELLOW SUBMARINE"
    puts decipher.update(ciphertext) + decipher.final

    puts "---"

    File.foreach("8.txt") do |line|
        puts "Detected repeated block: #{line}" if AESDetector.detect(line.strip.decode_hex)
    end
end
