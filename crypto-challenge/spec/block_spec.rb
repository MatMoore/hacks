require_relative "../src/block"

RSpec.describe Block::AesEcbCipher do
    it "is reversible" do
        cipher = Block::AesEcbCipher.new("YELLOW SUBMARINE")
        expect(cipher.decrypt(cipher.encrypt("foo"))).to eq "foo"
    end
end

