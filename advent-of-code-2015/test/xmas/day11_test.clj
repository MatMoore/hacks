(ns xmas.day11-test
  (:require [clojure.test :refer :all]
            [xmas.day11 :refer :all]))

(deftest inc-chars
  (is (= (inc-char \a) \b))
  (is (= (inc-char \h) \j))
  (is (= (inc-char \z) \a))
)

(deftest inc-string-test
  (is (= (inc-string "a") "b"))
  (is (= (inc-string "bz") "ca"))
  (is (= (inc-string "az") "ba"))
)

(deftest valid-pass
  (is (true? (is-valid "aabbcd"))))

(deftest missing-pair
  (is (false? (is-valid "abbcd"))))

(deftest is-straight-yes
  (is (true? (is-straight (seq "abc")))))

(deftest is-straight-no
  (is (false? (is-straight (seq "abb")))))

(deftest missing-straight
  (is (false? (is-valid "aabbc"))))
