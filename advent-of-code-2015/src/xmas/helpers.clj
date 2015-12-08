(ns xmas.helpers
)

(defn parse-int
  [s]
  (Integer/parseInt s))

(defn read-lines
  [filename]
  (with-open [rdr (clojure.java.io/reader filename)]
    (into [] (line-seq rdr))))
