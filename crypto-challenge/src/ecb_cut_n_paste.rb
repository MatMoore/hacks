require_relative "block"
require_relative "encode"

module Block
    using EncodeHelpers
    using Primitives

    class EcbUserProfile
        def initialize
            @uid = 0
            @cipher = AesEcbCipher.with_random_key
        end

        def create_encrypted_profile(email)
            @cipher.encrypt(profile_for(email))
        end

        def is_admin?(profile)
            profile = load_encrypted_profile(profile)
            return false if profile["email"].nil?
            return false if profile["uid"].nil?
            profile["role"] == "admin"
        end

    private

        def load_encrypted_profile(profile)
            @cipher.decrypt(profile).decode_uri_params
        end

        def profile_for(email)
            @uid += 1
            {email: email, uid: @uid, role: "user"}.encode_uri_params
        end
    end

    class EcbCutNPasteAttacker
        def initialize(oracle)
            @oracle = oracle
        end

        def make_admin_profile(blocksize: 16)
            admin_block = @oracle.create_encrypted_profile("A" * 10 + "admin".pad_to_size(blocksize))[blocksize, blocksize]

            # Try a bunch of different sized inputs until the blocks align,
            # and we can just replace the last one.
            # The length of the rest of the string is more or less stable so
            # this only takes a couple of tries.
            (0...blocksize).each do |offset|
                profile = @oracle.create_encrypted_profile("A" * offset + "A@attacker.com")
                tampered_profile = profile[0...-blocksize] + admin_block
                begin
                    if @oracle.is_admin?(tampered_profile)
                        return tampered_profile
                    end
                rescue OpenSSL::Cipher::CipherError
                    next
                end
            end

            nil
        end

    end


    if __FILE__ == $0
        puts EcbCutNPasteAttacker.new(EcbUserProfile.new).make_admin_profile.encode_hex
    end
end
