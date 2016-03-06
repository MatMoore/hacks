module Scoring
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
