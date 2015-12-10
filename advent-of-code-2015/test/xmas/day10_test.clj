(ns xmas.day10-test
  (:require [clojure.test :refer :all]
            [xmas.day10 :refer :all]))

(deftest count-one-one
  (is (= (count-digits "1") '([1 \1])))
)

(deftest look-and-say-one
  (is (= (look-and-say "1") "11"))
)

(deftest look-and-say-one-one
  (is (= (look-and-say "11") "21"))
)

(deftest look-and-say-two-one
  (is (= (look-and-say "21") "1211"))
)

(deftest look-and-say-one-two-one-one
  (is (= (look-and-say "1211") "111221"))
)

(deftest look-and-say-five-times
  (is (= (repeat-look-and-say "1" 5) "312211"))
)
