require_relative 'encode'
require_relative 'primitives'
require_relative "scoring"

module SingleByteXor
    using Primitives

    def self.best_guess(cyphertext, scorer: Scoring::dictionary_scorer)

        best = nil
        best_score = 0

        ('A'..'z').each do |key|
            full_key = key * cyphertext.length
            plaintext = cyphertext.xor(full_key)
            score = scorer.score_text(plaintext)
            if score > best_score
                best = plaintext
                best_score = score
            end
        end

        best
    end

    if __FILE__ == $0
        using EncodeHelpers

        cyphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736".decode_hex
        puts best_guess(cyphertext)
    end
end
