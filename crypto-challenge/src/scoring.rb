require_relative "primitives"

module Scoring
    using Primitives

    def self.frequency_count(text)
        count = Hash.new(0)
        text.each_char do |char|
            count[char] += 1
        end

        count
    end

    def self.load_words(path: '/usr/share/dict/words')
        IO.readlines(path).map(&:strip).join(' ')
    end

    def self.dictionary_scorer
        FrequencyScorer.from_text(load_words)
    end

    class KeysizeFinder
        attr_reader :text

        def initialize(text)
            @text = text
        end

        def evaluate_keysize(keysize)
            blocks = text.chars.each_slice(keysize).take(4).map(&:join)
            d1 = blocks[0].hamming_distance(blocks[1])
            d2 = blocks[1].hamming_distance(blocks[2])
            d3 = blocks[2].hamming_distance(blocks[3])
            d4 = blocks[0].hamming_distance(blocks[2])
            d5 = blocks[0].hamming_distance(blocks[3])
            d6 = blocks[1].hamming_distance(blocks[3])
            [keysize, (d1 + d2 + d3 + d4 + d5 + d6) / (6.0 * keysize)]
            # FIXME
        end

        def best_keysize(range)
            puts "best:"
            puts range.map(&method(:evaluate_keysize)).sort_by(&:last).to_s
            range.map(&method(:evaluate_keysize)).min_by(&:last).first
        end
    end

    class FrequencyScorer
        attr_reader :frequencies

        def initialize(frequencies)
            @frequencies = frequencies
        end

        def self.from_text(text)
            new(Scoring::frequency_count(text))
        end

        def score_text(text)
            text_freqs = Scoring::frequency_count(text.downcase)

            score = 0
            frequencies.each do |char, weight|
                score += text_freqs[char] * weight
            end

            score
        end
    end
end
