(ns xmas.day14
  (:require [xmas.helpers :refer :all])
)

(def reindeer-regex
  #"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds"
)

(defn parse-reindeer
  [acc line]
  (let [[match reindeer-name flyspeed flyseconds restseconds] (re-find reindeer-regex line)]
    (conj acc [reindeer-name (cycle (concat (repeat (parse-int flyseconds) (parse-int flyspeed)) (repeat (parse-int restseconds) 0)))])
    )
  )

(defn parse-reindeers
  [lines]
  (reduce parse-reindeer [] lines)
  )

(def day14-input (parse-reindeers (read-lines "day14.txt")))

(defn distance-travelled
  [[reindeer-name reindeer-speed]]
  [reindeer-name (reductions + reindeer-speed)]
)

(defn cumulative-reindeer-distance
  [n [reindeer-name reindeer-speed]]
  [
   reindeer-name
   (first
     (drop (dec n)
      (second (distance-travelled [reindeer-name reindeer-speed]))))
   ])

(defn distance-travelled-after
  [n reindeer-info]
  (second
    (cumulative-reindeer-distance n reindeer-info))
  )

(defn winner
  [reindeers n]
  (apply max (map (partial distance-travelled-after n) reindeers))
  )

(defn winning-reindeer
  [reindeers n]
  (let [reindeer-locations (map #(cumulative-reindeer-distance n %) reindeers)
        furthest-distance (apply (partial max-key second) reindeer-locations)]
    (map first
      (filter
        #(= (second %) (second furthest-distance))
      reindeer-locations))))

(println (winning-reindeer day14-input 2))

(defn winner2
  [reindeers n]
  (frequencies
    (mapcat #(winning-reindeer reindeers %) (range 1 (inc n)))))

(def example
  ["Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds"
   "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds"])

(defn day14-solution
  []
  [(winner day14-input 2503) (winner2 day14-input 2503)]
  )
