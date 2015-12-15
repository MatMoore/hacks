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
  [n reindeer-info]
  (drop (dec n)
    (second (distance-travelled reindeer-info))))

(defn distance-travelled-after
  [n reindeer-info]
  (first
    (cumulative-reindeer-distance n reindeer-info))
  )

(defn winner
  [reindeers n]
  (apply max (map (partial distance-travelled-after n) reindeers))
  )

(defn winning-reindeer
  [reindeers n]
  (first (apply (partial max-key second) (map (partial cumulative-reindeer-distance n) reindeers)))
  )

(println (map (partial cumulative-reindeer-distance n) reindeers))
(println (winning-reindeer day14-input 2))

(defn winner2
  [reindeers n]
  (reduce
    (fn [acc reindeer-name]
      (assoc-in
        acc
        [reindeer-name]
        (inc (get acc reindeer-name 0))
      ))
    {}
    (map
      (partial winning-reindeer reindeers)
      (range 1 (inc n)))))

(defn day14-solution
  []
  [(winner day14-input 2503) (winner2 day14-input 2503)]
  )
