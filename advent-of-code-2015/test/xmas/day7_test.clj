(ns xmas.day7-test
  (:require [clojure.test :refer :all]
            [xmas.day7 :refer :all]))

(def test-data
  (with-open [rdr (clojure.java.io/reader "day7test.txt")]
    (into {} (map parse-expression (line-seq rdr)))))

(deftest example-data
  (is (= (evaluate-wires test-data "d") 72))
  (is (= (evaluate-wires test-data "e") 507))
  (is (= (evaluate-wires test-data "f") 492))
  (is (= (evaluate-wires test-data "g") 114))
  (is (= (evaluate-wires test-data "h") 65412))
  (is (= (evaluate-wires test-data "i") 65079))
  (is (= (evaluate-wires test-data "x") 123))
  (is (= (evaluate-wires test-data "y") 456))
)
