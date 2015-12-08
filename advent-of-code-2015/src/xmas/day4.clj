(ns xmas.day4
  (:require [xmas.helpers :refer :all])
  (:require [digest :refer [md5]])
)

(def day4-secret-key "iwrupvqb")

(def day4-inputs
  (map #(str day4-secret-key %) (range)))

(defn advent-coins
  [prefix]
  (filter #(.startsWith (md5 %) prefix) day4-inputs))

(defn first-advent-coin
  [prefix]
  (first (advent-coins prefix)))

(defn day4-solution
  []
  [(first-advent-coin "00000") (first-advent-coin "000000")]
)
