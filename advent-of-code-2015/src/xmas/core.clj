(ns xmas.core
  (:gen-class))

(def task1-data (slurp "task1.txt"))

(def sanitised-data
  (filter #(contains? (set "()") %) task1-data))

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

(defn -main
  "Solve the last task"
  [& args]
  (println (pr-str first-symbol-for-basement)))
