require_relative 'encode'
require_relative 'primitives'
require "OpenSSL"

module Block
    using Primitives

    def self.cbc_decrypt(ciphertext, iv, blocksize: 16)
        output = ''
        block_ct = iv
        ciphertext.chars.each_slice(blocksize) do |block|
            output << (yield block.join).xor(block_ct)
            block_ct = block.join
        end

        output
    end

    class AesEcbCipher
        def initialize(key)
            @key = key
            @cipher = OpenSSL::Cipher.new("aes-128-ecb")
        end

        def encrypt(plaintext)
            cipher = @cipher.encrypt
            cipher.key = @key
            cipher.update(plaintext) + cipher.final
        end

        def decrypt(ciphertext, no_padding: false)
            cipher = @cipher.decrypt
            cipher.key = @key
            cipher.padding = 0 if no_padding
            cipher.update(ciphertext) + cipher.final
        end
    end
end

if __FILE__ == $0
    using EncodeHelpers

    ciphertext = IO.read("data/10.txt").gsub("\n", "").decode_base64

    iv = "\x00" * 16

    cipher = Block::AesEcbCipher.new("YELLOW SUBMARINE")

    puts (Block.cbc_decrypt(ciphertext, iv) do |block|
        cipher.decrypt(block, no_padding: true)
    end)
end
