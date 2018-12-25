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

        def encrypt(plaintext)
            @cipher.encrypt(plaintext + @unknown_string)
        end
    end

    class EcbPrefixOracle
        def initialize(blocksize: 16)
            key = SecureRandom.random_bytes(blocksize)
            @random_prefix = SecureRandom.random_bytes(1 + SecureRandom.random_number(2 * blocksize))
            @cipher = Block::AesEcbCipher.new(key)
            @unknown_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK".decode_base64
        end

        def encrypt(plaintext)
            @cipher.encrypt(@random_prefix + plaintext + @unknown_string)
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
                size_difference = @oracle.encrypt(plaintext).length - plaintext.length
                unless last.nil?
                    jump = size_difference - last
                    highest_jump = jump if jump > highest_jump
                end

                last = size_difference
            end

            highest_jump + 1
        end

        # Find how many random bytes there are in front of the attacker
        # controlled string in the plaintext. We can see this in the ciphertext
        # by repeating a character and gradually increasing the size of the
        # string until we see two repeated blocks. This tells us how many
        # random prefix blocks there are, and how many bytes to prefix
        # with to ensure that our attacker controller text aligns with
        # block boundaries.
        def measure_prefix(blocksize)
            (0...blocksize).each do |byte_offset|
                attacker_text = "A" * (blocksize * 2 + byte_offset)
                ciphertext = @oracle.encrypt(attacker_text)

                ct_blocks = ciphertext.chars.each_slice(blocksize).to_a
                ct_blocks.zip(ct_blocks[1..-1]).each_with_index do |(current_block, next_block), block_number|
                    if current_block == next_block
                        return [block_number, byte_offset]
                    end
                end
            end

            throw "Failed to create duplication in ciphertext blocks"
        end

        def decrypt
            output = ""
            blocksize = determine_blocksize
            block = nil
            prefix_blocks, alignment_prefix = measure_prefix(blocksize)

            0.step do |block_number|
                block, last = decrypt_block(
                    block_number: block_number,
                    blocksize: blocksize,
                    preceding_block: block,
                    alignment_prefix: "A" * alignment_prefix,
                    prefix_blocks: prefix_blocks
                )
                output << block
                break if last
            end

            output
        end

        # block_number is the block number to decrypt minus the number of prefix blocks
        # prefix_blocks is the number of blocks from our random prefix + alignment prefix
        # alignment_prefix is a prefix we insert into the attacker text, to make the random
        # prefix align with block boundaries.
        # preceding_block is the last block decrypted
        def decrypt_block(block_number:, blocksize:, alignment_prefix: "", prefix_blocks: 0, preceding_block: nil)
            decrypted = ""
            preceding_block ||= "A" * blocksize

            # Work out block boundaries for the block we're decrypting
            block_start = (prefix_blocks + block_number) * blocksize
            next_block_start = block_start + blocksize

            # Work out block boundaries for a test block we create
            # This block is right after the random and alignment prefixes
            test_block_start = prefix_blocks * blocksize
            next_test_block_start = test_block_start + blocksize

            is_last_block = false

            (1..blocksize).each do |byte_number|
                # Shift the next unknown byte into the last byte of the
                # preceding block, which is known - it's either the last block
                # decrypted or the prefix itself.
                preceding_part = preceding_block[byte_number, blocksize]

                oracle_result = @oracle.encrypt(alignment_prefix + preceding_part)

                # Extract the block of ciphertext we're examining.
                # This corresponds to the plaintext we manipulated above to
                # begin with our known prefix and end with the byte to be
                # decrypted next.
                oracle_block = oracle_result[block_start...next_block_start]

                # Use the oracle to test all possible plaintexts for the block
                # we're interested in, by varying the last byte.
                ("\x00".."\x7f").each do |char|
                    test_result = @oracle.encrypt(
                        alignment_prefix + preceding_part + decrypted + char
                    )
                    test_result_block = test_result[test_block_start...next_test_block_start]

                    if test_result_block == oracle_block
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
        puts "Byte-at-a-time ECB decryption (easy)"
        oracle = EcbOracle.new
        decryptor = EcbDecryptor.new(oracle)
        puts "Block size = #{decryptor.determine_blocksize}"
        puts "Random prefix: #{decryptor.measure_prefix(decryptor.determine_blocksize)}"
        puts "Using ECB = #{ECBDetector.detect(oracle.encrypt("a" * 200))}"
        puts decryptor.decrypt

        puts
        puts "Byte-at-a-time ECB decryption (harder)"
        oracle = EcbPrefixOracle.new
        decryptor = EcbDecryptor.new(oracle)
        puts "Block size = #{decryptor.determine_blocksize}"
        puts "Random prefix: #{decryptor.measure_prefix(decryptor.determine_blocksize)}"
        puts "Using ECB = #{ECBDetector.detect(oracle.encrypt("a" * 200))}"
        puts decryptor.decrypt

    end

end
