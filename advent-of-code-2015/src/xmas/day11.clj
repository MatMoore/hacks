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

(defn inc-string
  [character & string]
  (let [next-character (char (inc-char character))]
    (if (= next-character \a)
      (str next-character (inc-string string))
      (str next-character string))
    )
  )

(defn has-duplicate
  [char1 char2 & string]
  (= char1 char2)
  )

(defn inc-string-without-duplicate
  [string]
  (let [next-string (inc-string string)]
  (if (has-duplicate next-string)
    (recur next-string)
    next-string
    ))
  )

(defn reverse-inc-string
  [string]
  (reverse (inc-string-without-duplicate (reverse string)))
  )

(defn day11-solution
  []
  [])

