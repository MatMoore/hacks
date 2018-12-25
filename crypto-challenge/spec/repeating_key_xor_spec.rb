require_relative "../src/repeating_key_xor"

RSpec.describe RepeatingKeyXor, "#unravel" do
    it "gathers together characters a fixed distance apart" do
        ct = "abcabcabc"
        expect(RepeatingKeyXor::unravel(ct, 3)).to eq ["aaa", "bbb", "ccc"]
    end

    it "leaves shorter substrings when the text is not a multiple of the keysize" do
        ct = "abcabcabc"
        expect(RepeatingKeyXor::unravel(ct, 2)).to eq ["acbac", "bacb"]
    end
end


RSpec.describe RepeatingKeyXor, "#ravel" do
    it "interleaves each element together to form a single string" do
        parts = ["aaa", "bbb", "cc"]
        expect(RepeatingKeyXor::ravel(parts)).to eq "abcabcab"
    end
end
