(ns xmas.day12
  (:require [xmas.helpers :refer :all])
  (:require [clojure.data.json :refer [read-str]])
)

(def input (read-str (slurp "day12.txt")))

(derive clojure.lang.PersistentArrayMap ::json-object)
(derive clojure.lang.PersistentHashMap ::json-object)
(derive clojure.lang.PersistentVector ::json-array)
(derive java.lang.Double ::json-number)
(derive java.lang.Long ::json-number)

(defmulti extract-numbers class)

(defmethod extract-numbers ::json-object
  [jsonval]
  (let
    [values (vals jsonval)]
    (if (.contains values "red")
      '()
      (mapcat extract-numbers values))))

(defmethod extract-numbers ::json-array
  [jsonval]
  (mapcat
    extract-numbers
    jsonval))

(defmethod extract-numbers ::json-number
  [jsonval]
  (list jsonval))

(defmethod extract-numbers :default
  [jsonval]
  '())

(defn sum-all-numbers
  [jsonobj]
  (reduce + (extract-numbers jsonobj)))

(defn day12-solution
  []
  [(sum-all-numbers input)])
