require_relative "../src/encode.rb"

using EncodeHelpers

RSpec.describe String do
    describe "#decode_uri_params" do
        it "parses a single key value pair" do
            expect("foo=bar".decode_uri_params).to eq({"foo" => "bar"})
        end

        it "parses multiple key value pairs" do
            expect("foo=bar&bar=foo&baz=foobar".decode_uri_params).to eq({"foo" => "bar", "bar" => "foo", "baz" => "foobar"})
        end

        it "decodes percent literals" do
            expect("foo=bar%20bar&bar=foo%20foo".decode_uri_params).to eq({"foo" => "bar bar", "bar" => "foo foo"})
        end

        it "ignores trailing ampersands" do
            expect("foo=bar&".decode_uri_params).to eq({"foo" => "bar"})
        end

        it "ignores duplicate ampersands" do
            expect("foo=bar&&bar=foo".decode_uri_params).to eq({"foo" => "bar", "bar" => "foo"})
        end

        it "treats missing keys as empty string" do
            expect("foo=bar&=foo".decode_uri_params).to eq({"foo" => "bar", "" => "foo"})
        end

        it "treats missing values as empty string" do
            expect("foo=bar&bar=".decode_uri_params).to eq({"foo" => "bar", "bar" => ""})
        end
    end
end


RSpec.describe Hash do
    describe "#encode_uri_params" do
        it "encodes multiple key value pairs" do
            expect({"foo" => "bar", "bar" => "foo"}.encode_uri_params).to eq("foo=bar&bar=foo")
        end

        it "stringifies keys and values" do
            expect({foo: "bar", "bar" => 1}.encode_uri_params).to eq("foo=bar&bar=1")
        end

        it "encodes reserved characters" do
            expect({"foo" => "1+1=2", "bar" => "foo & bar"}.encode_uri_params).to eq("foo=1+1%3D2&bar=foo %26 bar")
        end
    end
end
