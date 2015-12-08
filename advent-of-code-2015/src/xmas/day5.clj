(ns xmas.day5
  (:require [xmas.helpers :refer :all])
)

(def day5-data
  (read-lines "day5.txt"))

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
  (filter nice? day5-data))

(def nice-list2
  (filter really-nice? day5-data))

(def number-nice
  (count nice-list))

(def number-nice2
  (count nice-list2))

(defn day5-solution
  []
  [number-nice number-nice2]
)
