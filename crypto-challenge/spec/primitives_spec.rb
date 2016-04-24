require_relative "../src/primitives"

using Primitives

RSpec.describe String do
    describe "#validate_padding" do
        it "returns true for valid padding" do
            valid = "ICE ICE BABY\x04\x04\x04\x04"
            expect{valid.padding_valid?}.to_not raise_error
        end

        it "raises an exception for invalid padding" do
            invalid = "ICE ICE BABY\x05\x05\x05\x05"
            invalid2 = "ICE ICE BABY\x01\x02\x03\x04"
            expect{invalid.padding_valid?}.to raise_error(SecurityError)
            expect{invalid2.padding_valid?}.to raise_error(SecurityError)
        end
    end
end

