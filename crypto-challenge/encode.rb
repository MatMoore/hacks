module EncodeHelpers
    refine String do
        def decode_hex
            [self].pack('H*')
        end

        def encode_hex
            unpack('H*').first
        end

        def encode_base64
            [self].pack('m0')
        end

        def decode_base64
            unpack('m0')
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
