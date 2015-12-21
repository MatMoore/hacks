(ns xmas.day20
  (:require [xmas.helpers :refer :all])
)

(def target 33100000)

(def elves (iterate inc 1))
(def houses (iterate inc 1))

(defn presents-for-elf
  [elf]
  (iterate (partial + elf) elf))

(def delivery-routes
  (map presents-for-elf elves))

(defn find-number
  [end-house delivery-routes]
  (take-while #(<= % end-house) delivery-routes))

(defn count-presents
  [house-number]
  (count
    (filter (partial = house-number)
    (flatten
      (take-while
        (comp not empty?)
        (map
          (partial find-number house-number)
          delivery-routes))))))

(defn day20-solution
  []
  (map count-presents (take 10 houses)))
