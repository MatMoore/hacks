require_relative 'encode'
require "OpenSSL"

if __FILE__ == $0
    using EncodeHelpers

    decipher = OpenSSL::Cipher.new("aes-128-ecb").decrypt
    ciphertext = IO.read("7.txt").gsub("\n", "").decode_base64
    decipher.key = "YELLOW SUBMARINE"
    puts decipher.update(ciphertext) + decipher.final
end
