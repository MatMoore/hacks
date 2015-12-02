(ns xmas.core
  (:require [clojure.string :refer [split]])
  (:gen-class))

(defn parse-int
  [s]
  (Integer/parseInt s))

(def task1-data (slurp "task1.txt"))

(def sanitised-data
  (filter #(contains? (set "()") %) task1-data))

(def day2-data
  (with-open [rdr (clojure.java.io/reader "day2.txt")]
    (into '() (line-seq rdr))))

(def day2-dimensions
  (map #(map parse-int (split % #"x")) day2-data))

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

(defn -main
  "Solve the last task"
  [& args]
  (println (pr-str total-ribbon-length)))
