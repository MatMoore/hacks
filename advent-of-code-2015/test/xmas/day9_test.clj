(ns xmas.day9-test
  (:require [clojure.test :refer :all]
            [xmas.day9 :refer :all]))

(def test-data
  ["London to Dublin = 464"
   "London to Belfast = 518"
   "Dublin to Belfast = 141"])

(def test-permutation ["foo" "bar" "baz"])

(def test-distances {#{"foo" "bar"} 1 #{"bar" "baz"} 2})

(deftest example-data
  (is (= (part1-solution test-data) 605))
)

(deftest example-perm-journey
  (is (= (permutation-journeys test-distances test-permutation) '(1 2))))

(deftest example-perm-length
  (is (= (permutation-length test-distances test-permutation) 3)))
