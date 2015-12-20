(ns xmas.day17
  (:require [xmas.helpers :refer :all])
  (:require [clojure.math.combinatorics :refer [subsets]])
)
(def containers [50 44 11 49 42 46 18 32 26 40 21 7 18.0 43 10 47 36 24 22 40.0])
(def containers-test [20 15 10 5 5.0])

(defn fit-eggnog
  [containers amount]
  (filter #(= (float amount) (float (reduce + %))) (subsets containers))
  )

(defn eggnog-fits
  [containers amount]
  (frequencies (map count (fit-eggnog containers amount)))
  )

(defn day17-solution
  []
  [(count (fit-eggnog containers 150)) (eggnog-fits containers 150)])
