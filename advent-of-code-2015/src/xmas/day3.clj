(ns xmas.day3
  (:require [xmas.helpers :refer :all])
  (:require [clojure.set :refer [union]])
)

(def day3-data
  (filter
    #(contains? (set ">v<^") %)
    (slurp "day3.txt")))

(def sleigh-directions
  {\> [1 0]
   \v [0 1]
   \< [-1 0]
   \^ [0 -1]})

(defn translate-sleigh
  "Move Santas sleigh according one space in the given direction"
  [[x y] direction]
  (let [diff (get sleigh-directions direction)]
    [(+ x (first diff)) (+ y (second diff))]))

(defn register-sleigh-movement
  "Update a count of visited houses, given the current position and a direction"
  [[history current-pos] direction]
  (let [new-pos (translate-sleigh current-pos direction)]
    [(assoc-in history [new-pos] (+ 1 (get history new-pos 0)))
     new-pos]))

(defn count-sleigh-visits
  "Count every house Santa visits, given a sequence of directions"
  [directions]
  (reduce register-sleigh-movement [{[0 0] 1} [0 0]] directions))

(def visited-houses
  "Get the set of visited houses for a sequence of directions"
  (comp set keys first count-sleigh-visits))

(def at-least-one-present
  "Number of houses with at least one present pre-robo-santa"
  (count (first (count-sleigh-visits day3-data))))

(def human-santa-directions (take-nth 2 day3-data))
(def robo-santa-directions (take-nth 2 (rest day3-data)))

(def assisted-least-one-present
  "Number of houses with at least one present post-robo-santa"
  (count
    (union
      (visited-houses human-santa-directions)
      (visited-houses robo-santa-directions))))

(defn day3-solution
  []
  [at-least-one-present assisted-least-one-present])
