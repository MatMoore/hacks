(ns xmas.day11-test
  (:require [clojure.test :refer :all]
            [xmas.day11 :refer :all]))

(deftest inc-chars
  (is (= (inc-char \a) \b))
  (is (= (inc-char \h) \j))
  (is (= (inc-char \z) \a))
)

(deftest inc-string-without-duplicate-test
  (is (= (inc-string-without-duplicate "a") "b"))
  (is (= (inc-string-without-duplicate "zb") "ac"))
  (is (= (inc-string-without-duplicate "za") "ab"))
)
