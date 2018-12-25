(ns xmas.day9
  (:require [xmas.helpers :refer :all])
  (:require [clojure.math.combinatorics :as combo])
)

(def day9-data (read-lines "day9.txt"))

(def line-regex #"(\w+) to (\w+) = (\d+)")

(defn parse-city
  [[distances cities] line]
  (let
    [[match from to distance-str] (re-find line-regex line)
     distance (parse-int distance-str)]
    [(assoc-in distances [#{from to}] distance)
     (conj cities from to)]))

(defn parse-cities
  [lines]
  (reduce parse-city [{} #{}] lines)
)

(defn permutation-journeys
  "Distances for each leg of a particular route"
  [distances perm]
  (let [pairs (map vector perm (rest perm))]
    (map #(get distances (set %)) pairs)))

(defn permutation-length
  "Total distance of a route"
  [distances perm]
  (reduce + (permutation-journeys distances perm)))

(defn travelling-santa-paths
  "All possible path lengths"
  [distances cities]
  (for
    [perm (combo/permutations cities)]
    (permutation-length distances perm)))

(defn travelling-santa-best
  "Length of the Santa's best route"
  [metric [distances cities]]
  (apply metric (travelling-santa-paths distances cities)))

(defn part1-solution
  [data]
  (travelling-santa-best min (parse-cities data)))

(defn part2-solution
  [data]
  (travelling-santa-best max (parse-cities data)))

(defn day9-solution
  []
  [(part1-solution day9-data) (part2-solution day9-data)])
