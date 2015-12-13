(ns xmas.day12-test
  (:require [clojure.test :refer :all]
            [xmas.day12 :refer :all]))

(deftest extract-single-number
  (is (= (extract-numbers 2.0)
         '(2.0))))

(deftest extract-number-array
  (is (= (extract-numbers [1.0 2.0 3.0])
         '(1.0 2.0 3.0))))

(deftest extract-number-obj
  (is (= (extract-numbers {:foo 1.0})
         '(1.0))))

(deftest extract-nested
  (is (= (extract-numbers {:foo [1.0 [2.0 3.0]]})
         '(1.0 2.0 3.0))))

(deftest extract-balanced
  (is (= (extract-numbers {"a" [-1,1]})
         '(-1 1))))

(deftest extract-nested2
  (is (= (extract-numbers {"a" {"b" 4},"c" -1})
         '(4 -1))))

(deftest extract-nested3
  (is (= (extract-numbers [[[3]]])
         '(3))))
