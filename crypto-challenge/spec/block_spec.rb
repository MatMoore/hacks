require "securerandom"
require_relative "../src/block"

RSpec.describe Block::AesEcbCipher do
    it "is reversible" do
        cipher = Block::AesEcbCipher.new("YELLOW SUBMARINE")
        expect(cipher.decrypt(cipher.encrypt("foo"))).to eq "foo"
    end
end

using EncodeHelpers
using Primitives

RSpec.describe "Cipher block chaining" do

    context "With a long plaintext" do
        it "is reversible" do
            start = "a quick brown fox jumps over the lazy dog"
            iv = SecureRandom.random_bytes(16)
            cipher = Block::AesEcbCipher.new(SecureRandom.random_bytes(16))
            encrypted = Block.cbc_encrypt(start, iv, &cipher.method(:encrypt_block))
            decrypted = Block.cbc_decrypt(encrypted, iv, &cipher.method(:decrypt_block))

            expect(decrypted).to eq start
        end
    end

    context "With a single block of plaintext" do
        it "is reversible" do
            start = "hello worldddddd"
            iv = "\x00" * 16
            cipher = Block::AesEcbCipher.new("YELLOW SUBMARINE")

            encrypted = Block.cbc_encrypt(start, iv, &cipher.method(:encrypt_block))

            decrypted = Block.cbc_decrypt(encrypted, iv, &cipher.method(:decrypt_block))

            expect(decrypted).to eq start
        end

        describe "#cbc_encrypt" do
             it "returns a new string with the same length plus padding bytes" do
                start = "hello worldddddd"
                padding = "\x10" * 16
                padded = start + padding
                iv = "\x01" * 16
                cipher = Block::AesEcbCipher.new("YELLOW SUBMARINE")

                encrypted = Block.cbc_encrypt(start, iv, &cipher.method(:encrypt_block))

                expect(encrypted).not_to eq start
                expect(encrypted.length).to eq padded.length
            end

            it "is equal to ECB(block XOR IV) if you ignore padding bytes" do
                start = "hello worldddddd"
                iv = "\x01" * 16
                cipher = Block::AesEcbCipher.new("YELLOW SUBMARINE")

                cbc_encrypted = Block.cbc_encrypt(start, iv, &cipher.method(:encrypt_block))
                ecb_encrypted = cipher.encrypt(start.xor(iv))

                # Padding bytes differ because CBC applies it prior to XORing the IV.
                expect(cbc_encrypted[0...16].encode_hex).to eq ecb_encrypted[0...16].encode_hex

            end
        end
    end
end

