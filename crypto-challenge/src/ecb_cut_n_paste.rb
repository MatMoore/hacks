require_relative "block"
require_relative "encode"

module Block
    using EncodeHelpers

    class EcbUserProfile
        def initialize
            @uid = 0
            @cipher = AesEcbCipher.with_random_key
        end

        def create_encrypted_profile(email)
            @cipher.encrypt(profile_for(email))
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

    end


    if __FILE__ == $0
        puts EcbUserProfile.new.create_encrypted_profile("alice@alicecorp.com").encode_hex
    end
end
