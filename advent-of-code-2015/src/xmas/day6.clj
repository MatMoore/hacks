(ns xmas.day6
  (:require [xmas.helpers :refer :all])
)

(def day6-data
  (read-lines "day6.txt"))

(defn toggle-light
  [lights coords]
  (assoc-in
    lights [coords]
    (not (get lights coords false))))

(defn set-light
  [state lights coords]
  (assoc-in lights [coords] state))

(defn set-light2
  [diff lights coords]
  (assoc-in lights [coords] (max 0 (+ diff (get lights coords 0)))))

(def turn-on-light2
  (partial set-light2 1))

(def turn-off-light2
  (partial set-light2 -1))

(def toggle-light2
  (partial set-light2 2))

(def turn-on-light
  (partial set-light true))

(def turn-off-light
  (partial set-light false))

(defn rect
  [[left top right bottom]]
  (for
    [x (range
         left (+ 1 right))
     y (range
         top (+ 1 bottom))]
    [x y]))

(defn run-light-instruction
  "Apply an instruction to the lights and return their new state"
  [lights [command corners]]
  (reduce command lights (rect corners)))

(def lights-regex
  #"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)")

(defn parse-light-instruction
  [line]
  (let [[match command & corners] (re-find lights-regex line)]
    (case command
      "turn on" [turn-on-light2 (map parse-int corners)]
      "turn off" [turn-off-light2 (map parse-int corners)]
      "toggle" [toggle-light2 (map parse-int corners)])))

(defn run-light-sequence
  "Follow Santa's instructions for setting up the lights"
  [instructions]
  (reduce
    run-light-instruction
    {}
    (map parse-light-instruction instructions)))

(defn total-brightness
  "Count the total brightness after following Santa's instructions"
  [instructions]
  (reduce +
    (vals
      (run-light-sequence instructions))))

(defn day6-solution
  []
  [(total-brightness day6-data)]
)
