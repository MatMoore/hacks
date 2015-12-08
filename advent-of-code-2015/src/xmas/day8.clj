(ns xmas.day8
  (:require [xmas.helpers :refer :all])
  (:require [clojure.string :refer [replace]])
)

(def day8-data (read-lines "day8.txt"))

(def replace-hex
  "Because the reader doesn't parse hex literals, just replace them with another letter"
  (fn [string] (replace string #"\\x[0-9a-fA-F]{2}" "X")))

(defn parse-list
  "Use the reader to decode Santa's list. They're almost the same as clojure string literals."
  [data]
  (map read-string (map replace-hex data)))

(defn name-diffs
  "Diff the length of the names before and after decoding"
  [data-before data-after] (map - (map count data-before) (map count data-after)))

(defn total-name-diffs
  [data-before data-after] (reduce + (name-diffs data-before data-after)))

(defn double-encode-name
  "Escape all double quotes and backslashes with another backslash"
  [string]
  (str
    "\""
    (replace string #"[\\\"]" #(str "\\" %))
    "\"" ))

(defn double-encode-list [data]
  (map double-encode-name data))

(def task8 (total-name-diffs (double-encode-list day8-data) day8-data))

(defn day8-solution
  []
  [(total-name-diffs day8-data (parse-list day8-data))
    (total-name-diffs (double-encode-list day8-data) day8-data)])
