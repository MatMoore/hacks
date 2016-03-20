module EncodeHelpers
    refine String do
        def decode_hex
            [self].pack('H*')
        end

        def encode_hex
            unpack('H*').first
        end

        def encode_hex_blocks(blocksize)
            chars.each_slice(blocksize).map(&:join).map {|x| x.encode_hex}.join('-')
        end

        def encode_base64
            [self].pack('m0')
        end

        def decode_base64
            unpack('m0')[0]
        end

        def decode_uri_params
            pairs = split('&')
            result = {}
            decode_percent_chars = lambda do |str|
                str.gsub(/%([0-9a-fA-F]{2})/) do |match|
                    [$1].pack('H')
                end
            end

            pairs.each do |pair|
                key, value = pair.split('=')
                next if key.nil?

                value ||= ""

                result[decode_percent_chars.call(key)] = decode_percent_chars.call(value)
            end

            result
        end
    end

    refine Hash do
        def encode_uri_params
            # Incomplete but good enough for the exercise
            encode_reserved = lambda do |str|
                str.gsub(/[=&]/) {|char| "%" + char.unpack('H*')[0].upcase}
            end

            encoded_pairs = []
            each_pair do |key, value|
                encoded_pairs << "#{encode_reserved.call(key.to_s)}=#{encode_reserved.call(value.to_s)}"
            end
            encoded_pairs.join("&")
        end
    end
end


if __FILE__ == $0
    using EncodeHelpers
    hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    encoded = hex.decode_hex.encode_base64
    puts encoded
    puts encoded == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
end
