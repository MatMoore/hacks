require_relative 'encode'
require_relative 'primitives'
require "OpenSSL"

module Block
    using Primitives

    # These CBC methods perform their own padding, and take
    # a proc that performs block encryption/decryption
    # without padding.
    def self.cbc_decrypt(ciphertext, iv, blocksize: 16)
        output = ''
        prev_block_ct = iv
        ciphertext.chars.each_slice(blocksize) do |block|
            block_ct = block.join
            cipher_output = (yield block_ct)
            output << cipher_output.xor(prev_block_ct)
            prev_block_ct = block_ct
        end

        output.trim_padding
    end

    def self.cbc_encrypt(plaintext, iv, blocksize: 16)
        plaintext = plaintext.pad_to_size(blocksize)

        output = ''
        block_ct = iv
        plaintext.chars.each_slice(blocksize) do |block|
            cipher_input = block.join.xor(block_ct)
            block_ct = (yield cipher_input)
            output << block_ct
        end

        output
    end

    class AesEcbCipher
        def initialize(key)
            @key = key
        end

        def encrypt_block(plaintext)
            encrypt(plaintext, no_padding: true)
        end

        def decrypt_block(plaintext)
            decrypt(plaintext, no_padding: true)
        end

        def encrypt(plaintext, no_padding: false)
            cipher = build_cipher.encrypt
            cipher.key = @key
            cipher.padding = 0 if no_padding
            cipher.update(plaintext) + cipher.final
        end

        def decrypt(ciphertext, no_padding: false)
            cipher = build_cipher.decrypt
            cipher.key = @key
            cipher.padding = 0 if no_padding
            cipher.update(ciphertext) + cipher.final
        end

    private

        def build_cipher
            OpenSSL::Cipher.new("aes-128-ecb")
        end
    end

    def self.encryption_oracle(plaintext)
        prng = Random.new
        key = prng.bytes(16)
        prefix_size = prng.rand(5..10)
        postfix_size = prng.rand(5..10)
        padded = prng.bytes(prefix_size) + plaintext + prng.bytes(postfix_size)
        cipher = AesEcbCipher.new(key)
        if prng.rand > 0.5
            ciphertext = cipher.encrypt(padded)
            [:ecb, ciphertext]
        else
            iv = prng.bytes(16)
            ciphertext = Block.cbc_encrypt(padded, iv, &cipher.method(:encrypt_block))
            [:cbc, ciphertext]
        end
    end

    def self.ecb_encryption_oracle(plaintext)
        prng = Random.new
        key = prng.bytes(16)
        prefix_size = prng.rand(5..10)
        postfix_size = prng.rand(5..10)
        padded = prng.bytes(prefix_size) + plaintext + prng.bytes(postfix_size)
        cipher = AesEcbCipher.new(key)
        if prng.rand > 0.5
            ciphertext = cipher.encrypt(padded)
            [:ecb, ciphertext]
        else
            iv = prng.bytes(16)
            ciphertext = Block.cbc_encrypt(padded, iv, &cipher.method(:encrypt_block))
            [:cbc, ciphertext]
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
