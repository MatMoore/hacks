(ns xmas.day10
  (:require [xmas.helpers :refer :all])
  (:require [clojure.string :refer [split]])
)

(defn count-digits
  [digits]
  (map
    (fn [same-digits]
      [(count same-digits) (first same-digits)])
    (partition-by identity digits))
)

(defn look-and-say
  [last-number]
  (apply str (flatten (count-digits last-number)))
)

(defn repeat-look-and-say
  [last-number n]
  (if (> n 0)
    (recur
      (look-and-say last-number)
      (dec n))
    last-number)
)

(def input "1113122113"
)

(defn day10-solution
  []
  [(repeat-look-and-say input 40)]
  )
