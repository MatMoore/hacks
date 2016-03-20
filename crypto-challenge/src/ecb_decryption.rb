require "securerandom"
require_relative "encode"
require_relative "block"
require_relative "aes"

module EcbDecryption
    using EncodeHelpers

    class EcbOracle
        def initialize(blocksize: 16)
            key = SecureRandom.random_bytes(blocksize)
            @cipher = Block::AesEcbCipher.new(key)
            @unknown_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK".decode_base64
        end

        def encrypt_with_prefix(plaintext)
            @cipher.encrypt(plaintext + @unknown_string)
        end
    end

    class EcbDecryptor
        def initialize(oracle)
            @oracle = oracle
        end


        # Determine blocksize by increasing the plaintext a byte at a time
        # when we get to a multiple of the block size, the length of the
        # padding will go up by a whole block.
        def determine_blocksize(search_space: 2..64)
            highest_jump = 0
            last = nil
            search_space.each do |i|
                plaintext = "A" * i
                size_difference = @oracle.encrypt_with_prefix(plaintext).length - plaintext.length
                unless last.nil?
                    jump = size_difference - last
                    highest_jump = jump if jump > highest_jump
                end

                last = size_difference
            end

            highest_jump + 1
        end

        def decrypt
            output = ""
            blocksize = determine_blocksize
            block = nil
            0.step do |block_number|
                block, last = decrypt_block(
                    block_number: block_number,
                    blocksize: blocksize,
                    preceding_block: block
                )
                output << block
                break if last
            end

            output
        end

        def decrypt_block(block_number:, blocksize:, preceding_block: nil)
            decrypted = ""
            preceding_block ||= "A" * blocksize
            block_start = block_number * blocksize
            next_block_start = block_start + blocksize
            is_last_block = false

            (1..blocksize).each do |byte_number|
                # Shift the next unknown byte into the last byte of the
                # preceding block, which is known - it's either the last block
                # decrypted or the prefix itself.
                n_bytes_short = preceding_block[byte_number, blocksize]
                byte_short_prefix = n_bytes_short

                oracle_result = @oracle.encrypt_with_prefix(byte_short_prefix)

                # Extract the block of ciphertext we're examining.
                # This corresponds to the plaintext we manipulated above to
                # begin with our known prefix and end with the byte to be
                # decrypted next.
                oracle_block = oracle_result[block_start...next_block_start]

                # Use the oracle to test all possible plaintexts for the block
                # we're interested in, by varying the last byte.
                # Since this is ECB, we can place our test string at the start
                # and just ignore the ciphertext blocks after the first one.
                ("\x00".."\x7f").each do |char|
                    test_prefix = byte_short_prefix + decrypted + char
                    test_result = @oracle.encrypt_with_prefix(test_prefix)

                    if test_result[0...blocksize] == oracle_block
                        decrypted << char
                        break
                    end
                end

                # Stop when we can't decrypt anymore.
                is_last_block = decrypted.length < byte_number
            end


            [decrypted, is_last_block]
        end
    end

    if __FILE__ == $0
        oracle = EcbOracle.new
        decryptor = EcbDecryptor.new(oracle)
        puts "Block size = #{decryptor.determine_blocksize}"
        puts "Using ECB = #{ECBDetector.detect(oracle.encrypt_with_prefix("a" * 200))}"
        puts decryptor.decrypt
    end

end
