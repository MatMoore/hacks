(ns xmas.day2
  (:require [xmas.helpers :refer :all])
  (:require [clojure.string :refer [split]])
)

(def day2-data
  (read-lines "day2.txt"))

(def day2-dimensions
  (map #(map parse-int (split % #"x")) day2-data))

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

(defn day2-solution []
  [total-paper-for-all-presents total-ribbon-length])
