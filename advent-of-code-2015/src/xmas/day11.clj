(ns xmas.day11
  (:require [xmas.helpers :refer :all])
  (:require [clojure.string :refer [split]]))

(def input "hepxcrrq")

(def ascii-a (int \a))

(def forbidden-chars (set "iol"))

(defn inc-char
  "Get the next character in the lowercase alphabet minus {i, o, l}"
  [character]
  (let
    [next-code (inc (int character))
     letter-idx (mod (- next-code ascii-a) 26)
     wrapped-around (+ ascii-a letter-idx)
     next-char (char wrapped-around)]
    (if (contains? forbidden-chars next-char)
      (recur next-char)
      next-char)))

(defn inc-charvector
  "Increment a vector of characters, ignoring the rules for straights/pairs"
  [ca]
  (let [smallest (last ca)
       others (into [] (butlast ca))
       next-char (inc-char smallest)]
    (if (= next-char \a)
      (conj (inc-charvector others) next-char)
      (conj others next-char)
    )
  ))

(defn is-straight
  "Increasing straight of characters, e.g. abc bcd. Skipping letters doesn't count."
  [substr]
  (let
    [nums (map int substr)
     pairs (map vector nums (rest nums))
     diffs (map #(apply - %) pairs)]
    (every? (partial = -1) diffs)))

(defn is-valid
  "Does a string meet all three rules?"
  [string]
  (and
    (not (nil? (re-find #"(\w)\1.*(\w)\2" string)))
    (boolean (some
      is-straight
      (partition 3 1 string)))
  ))

(defn inc-string
  "Takes a string and returns the next possible one"
  [string]
  (apply str (inc-charvector (into [] string))))

(defn inc-valid-string
  "Takes a string and returns the next valid password"
  [string]
  (let [next-string (inc-string string)]
    (println next-string)
    (if (is-valid next-string)
      next-string
      (recur next-string))))

(defn day11-solution
  []
  (let [a (inc-valid-string input)
        b (inc-valid-string a)]
    [a b]))

