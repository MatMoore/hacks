(ns xmas.core
  (:require [clojure.string :refer [split]])
  (:require [clojure.set :refer [union]])
  (:require [digest :refer [md5]])
  (:gen-class))

(defn parse-int
  [s]
  (Integer/parseInt s))

(defn read-lines
  [filename]
  (with-open [rdr (clojure.java.io/reader filename)]
    (into [] (line-seq rdr))))

(def task1-data (slurp "task1.txt"))

(def sanitised-data
  (filter #(contains? (set "()") %) task1-data))

(def day2-data
  (read-lines "day2.txt"))

(def day2-dimensions
  (map #(map parse-int (split % #"x")) day2-data))

(def day3-data
  (filter
    #(contains? (set ">v<^") %)
    (slurp "day3.txt")))

(def day5-data
  (read-lines "day5.txt"))

(def day6-data
  (read-lines "day6.txt"))

(defn take-elevator
  "Go to the floor indicated by the symbol"
  [start-floor instruction]
  (+ start-floor (if (= \( instruction) 1 -1)))

(defn extract-last-floor
  "Get the last floor we were on given a vector of pos/floor pairs"
  [history]
  (if (empty? history)
    0
    (last (last history))))

(defn take-elevator-with-history
  "Go to the floor indicated by the symbol, maintaining a history of where we went"
  [history [seq-no instruction]]
  (let
    [pos (+ seq-no 1)
     floor (take-elevator (extract-last-floor history) instruction)]
    (conj history [pos floor])))

(defn find-floor
  "Find the floor santa ends up on after taking the lift up and down"
  [instructions]
  (reduce take-elevator 0 instructions))

(def task1
  (find-floor sanitised-data))

(def indexed-instructions (map vector (range) sanitised-data))

(def indexed-floors
  (reduce take-elevator-with-history [] indexed-instructions))

(defn visited-basement?
  "Given an elevator event, decide whether it was a basement visit"
  [[pos floor]]
  (= -1 floor))

(def not-visited-basement? (complement visited-basement?))

(def first-symbol-for-basement
  "Find the index of the first instruction that takes santa to the basement"
  (first
    (first
      (drop-while not-visited-basement? indexed-floors))))

(defn wrapping-sheets
  "Calculate dimensions of the sheets of wrapping paper required to cover sides of a cuboid"
  [[w h l]]
  [[l w] [l w] [w h] [w h] [h l] [h l]])

(def area (partial reduce *))
(def volume area)

(defn total-paper-for-present
  "Calculate total paper to wrap a cuboid"
  [dimensions]
  (let [sides (wrapping-sheets dimensions)
        sheet-areas (map area sides)]
    (reduce + (cons (apply min sheet-areas) sheet-areas))))

(def total-paper-for-all-presents
  (reduce + (map total-paper-for-present day2-dimensions)))

(defn wrapping-ribbon-length
  "The smallest perimeter of any one face"
  [dimensions]
  (* 2
     (reduce +
             (take 2 (sort dimensions)))))

(defn present-ribbon-length
  [dimensions]
  (+ (volume dimensions) (wrapping-ribbon-length dimensions)))

(def total-ribbon-length
  (reduce + (map present-ribbon-length day2-dimensions)))

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

(def day4-secret-key "iwrupvqb")

(def day4-inputs
  (map #(str day4-secret-key %) (range)))

(def advent-coins
  (filter #(.startsWith (md5 %) "000000") day4-inputs))

(defn first-advent-coin
  []
  (first advent-coins))

(def repeated-letter? #"(\w)\1")
(def three-vowels? #"(.*[aeiou]){3}")
(def bad-letter-pair? #"(ab)|(cd)|(pq)|(xy)")
(def repeated-pair? #"(\w\w).*\1")
(def three-letter-palindrome? #"(\w).\1")

(defn nice?
  [n]
  (and
    (not (empty? (re-seq repeated-letter? n)))
    (not (empty? (re-seq three-vowels? n)))
    (empty? (re-seq bad-letter-pair? n))))

(defn really-nice?
  [n]
  (and
    (not (empty? (re-seq repeated-pair? n)))
    (not (empty? (re-seq three-letter-palindrome? n)))))

(def nice-list
  (filter really-nice? day5-data))

(def number-nice
  (count nice-list))

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

(defn -main
  "Solve the last task"
  [& args]
  (println (pr-str (total-brightness day6-data))))
