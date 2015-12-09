(ns xmas.core
  (:require [xmas.day1 :refer [day1-solution]])
  (:require [xmas.day2 :refer [day2-solution]])
  (:require [xmas.day3 :refer [day3-solution]])
  (:require [xmas.day4 :refer [day4-solution]])
  (:require [xmas.day5 :refer [day5-solution]])
  (:require [xmas.day6 :refer [day6-solution]])
  (:require [xmas.day7 :refer [day7-solution]])
  (:require [xmas.day8 :refer [day8-solution]])
  (:require [xmas.day9 :refer [day9-solution]])
  (:gen-class))

(def resolve-string (comp resolve symbol))

(defn -main
  "Show a solution"
  [& args]
  (let [day (or (first args) "1")
        func-name (str "day" day "-solution")
        func (ns-resolve 'xmas.core (symbol func-name))]
    (println func-name)
    (println (pr-str (apply func [])))))
