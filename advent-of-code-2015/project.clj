(defproject xmas "0.1.0-SNAPSHOT"
  :description "Advent of code"
  :dependencies [
                 [org.clojure/clojure "1.7.0"]
                 [org.clojure/math.combinatorics "0.1.1"]
                 [digest "1.4.4"]]
  :main ^:skip-aot xmas.core
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
